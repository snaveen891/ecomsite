from celery import shared_task
from django.core.mail import send_mail
from.models import Order
@shared_task
def order_confirmation(order_id):
    try:
        order = Order.objects.get(id=order_id)
        subject = f'Order nr. {order.id}'
        message = (
            f'Dear {order.first_name},\n\n'
            f'Thank you for your order!\n\n'
            f'Order Details:\n'
            f'Order ID: {order.id}\n'
            f'Order Date: {order.created}\n'
            f'Total Amount: ${order.get_total_cost}\n\n'
            f'Shipping Address:\n'
            f'{order.address}\n'
            f'{order.city}, {order.postal_code}\n\n'
            f'We will notify you once your order is shipped.\n\n'
            f'Best regards,\n'
            f'The Ecomsite Team'
        )
        mail_sent = send_mail(
            subject, message, 'admin@ecomsite.com', [order.email]
        )
        return mail_sent
    except Order.DoesNotExist:
        return False