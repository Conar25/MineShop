from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

from cart.cart import Cart

from .forms import OrderForm
from .models import OrderItem, Order
from .tasks import send_order_created_email, send_order_paid_email
from .utils import write_invoice_pdf


def payment_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'order/payment.html', {'order': order})


def complete_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.paid = True
    order.payment_time = timezone.now()
    order.save()
    send_order_paid_email(pk)
    return redirect('shop:list')


def order_view(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            cart = Cart(request)
            order = order_form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            payment_url = request.build_absolute_uri(reverse('order:payment', args=[order.pk,]))
            send_order_created_email.delay(order.pk, order.email, payment_url)
            return redirect('order:payment', pk=order.pk)
    else:
        order_form = OrderForm()

    return render(request, 'order/order.html', {'order_form': order_form})


@staff_member_required
def invoice_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if not order.paid:
        return "Doesn't paid"
    response = HttpResponse(content_type="application/pdf")
    write_invoice_pdf(response, pk)
    response['Content-Disposition'] = f'attachment; filename="invoice_{pk}.pdf"'
    return response
