from io import BytesIO
from celery import shared_task
from django.shortcuts import get_object_or_404
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


@shared_task
def payment_completed(order_id):
    '''tarefa para enviar notificação por e-mail
    quando um pedido é criado com sucesso'''

    order = get_object_or_404(Order, id=order_id)
    # cria o e-mail para a fatura
    subject = f'My shop - EE Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase'
    email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])

    # gera o pdf
    html = render_to_string('orders/order/pdf.html', {'order': order})

    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # anexa o arquivo pdf
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
    email.send()
