from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from cart.cart import Cart
import razorpay
from .forms import OrderCreationForm, OrderCancellationForm
from .models import OrderItem, Order
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import hmac
import hashlib

from .tasks import order_confirmation

client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

@login_required
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
            return redirect('orders:payment', order.id)
    else:
        form = OrderCreationForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_context = {
        'order': order,
        'order_amount': order.get_total_cost(),
        'razorpay_order_id': order.razorpay_order_id,
        'razorpay_api_key': settings.RAZORPAY_API_KEY,
    }
    return render(request, 'orders/payment/pay.html', order_context)

@csrf_exempt
def frontend_verify(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        if client.utility.verify_payment_signature(data):
            order = Order.objects.get(razorpay_order_id=data['razorpay_order_id'])
            order.razorpay_payment_id = data['razorpay_payment_id']
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'failed'})

@login_required
def order_completed(request, order_id):
    return render(request, 'orders/order/completed.html', {'order_id': order_id})

@login_required
def order_failed(request, order_id):
    return render(request, 'orders/order/failed.html', {'order_id': order_id})

@csrf_exempt
def webhook_verify(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)
    try:
        payload = request.body
        received_signature = request.headers.get("X-Razorpay-Signature")
        expected_signature = hmac.new(
            settings.RAZORPAY_WEBHOOK_SECRET.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()

        data = json.loads(payload)
        order_id = data["payload"]["payment"]["entity"]["order_id"]
        payment_id = data["payload"]["payment"]["entity"]["id"]
        order = Order.objects.get(razorpay_order_id=order_id)
        print(received_signature, expected_signature)
        if expected_signature != received_signature:
            order.status = Order.Status.FAILED
            return JsonResponse({"error": "Invalid signature"}, status=400)

        data = json.loads(payload)

        order_id = data["payload"]["payment"]["entity"]["order_id"]
        payment_id = data["payload"]["payment"]["entity"]["id"]

        order = Order.objects.get(razorpay_order_id=order_id)
        order.razorpay_payment_id = payment_id
        order.razorpay_signature = received_signature
        order.status = Order.Status.PROCESSING
        order.paid = True
        order.save()
        order_confirmation.delay(order.id)
        return JsonResponse({"status": "success", "message": "Order updated"}, status=200)

    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found"}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order/order_detail.html', {'order': order})

@login_required
def cancel_order(request, order_id):
    if request.method == 'POST':
        form = OrderCancellationForm(request.POST)
        if form.is_valid():
            order = get_object_or_404(Order, id=order_id, user=request.user)
            cancellation = form.save(commit=False)
            cancellation.order = order
            cancellation.save()
            order.status = Order.Status.CANCELLATION_REQUESTED
            order.save()
            return redirect('orders:order_list')
    else:
        form = OrderCancellationForm()
        order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order/cancel.html', {'order': order, 'form': form})
