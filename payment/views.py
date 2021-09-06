from django.shortcuts import render

# Create your views here.
import braintree
from orders.models import Order
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .tasks import payment_completed
# intancia o gateway de pagamento braintree
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        # obtem nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # cria e subete a transação
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # marca o pedidocomo pago
            order.paid = True
            # armazena o ID de transação
            order.braintree_id = result.transaction.id
            order.save()
            payment_completed.delay(order.id)
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # gera o token
        client_token = gateway.client_token.generate()
        return render(request, 'payment/process.html', {'order': order, 'client_token': client_token})


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
