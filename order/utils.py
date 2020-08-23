import weasyprint

from django.shortcuts import get_object_or_404, reverse
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order

def write_invoice_pdf(out, pk):
    order = get_object_or_404(Order, pk=pk)
    html = weasyprint.HTML(string=render_to_string('order/invoice.html', {'order':order}))
    css = weasyprint.CSS(filename=settings.STATIC_ROOT / 'css/invoice.css')
    html.write_pdf(out, stylesheets=[css])
    return out
