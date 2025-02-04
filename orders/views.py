from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from cart.cart import Cart
import razorpay
from .forms import OrderCreationForm
from .models import OrderItem, Order
from django.shortcuts import get_object_or_404

from .tasks import order_created

client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.razorpay_order_id = client.order.create({'amount': int(cart.get_total_price()*100), 'currency': 'INR'})['id']
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            cart.clear()
            order_created.delay(order.id)
            return redirect('orders:payment', order.id)
    else:
        form = OrderCreationForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_context = {
        'order_amount': order.get_total_cost(),
        'razorpay_order_id': order.razorpay_order_id,
        'razorpay_api_key': settings.RAZORPAY_API_KEY,
    }
    return render(request, 'orders/payment/pay.html', order_context)

from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def frontend_verify(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})

def payment_done(request):
    return render(request, 'orders/payment/payment_done.html')


import hmac
import hashlib

@csrf_exempt
def webhook_verify(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        payload = request.body  # ✅ Get raw request body
        received_signature = request.headers.get("X-Razorpay-Signature")  # ✅ Get signature
        # ✅ Compute the correct HMAC SHA256 signature
        expected_signature = hmac.new(
            settings.RAZORPAY_WEBHOOK_SECRET.encode(),  # ✅ Use Razorpay secret key
            payload,  # ✅ Use raw payload
            hashlib.sha256
        ).hexdigest()
        print("🔍 Expected Signature:", expected_signature)
        print("🔍 Received Signature:", received_signature)
        # ✅ Compare the computed signature with the received signature
        if expected_signature != received_signature:
            return JsonResponse({"error": "Invalid signature"}, status=400)

        # ✅ Parse JSON payload
        data = json.loads(payload)

        # ✅ Extract order ID and payment ID from webhook payload
        order_id = data["payload"]["payment"]["entity"]["order_id"]
        payment_id = data["payload"]["payment"]["entity"]["id"]

        # ✅ Update Order in DB
        order = Order.objects.get(razorpay_order_id=order_id)
        order.razorpay_payment_id = payment_id
        order.razorpay_signature = received_signature
        order.paid = True
        order.save()

        return JsonResponse({"status": "success", "message": "Order updated"}, status=200)

    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found"}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
from django.contrib.auth.decorators import login_required

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order/order_detail.html', {'order': order})