from django.contrib import admin
from django.shortcuts import reverse
from django.utils.safestring import mark_safe

from .models import Order, OrderItem


def invoice(order):
    url = reverse('order:invoice', args=[order.pk])
    return mark_safe(f'<a href={url}>PDF</a>')


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid', invoice]
    list_filter = ['paid']
    inlines = [OrderItemInline]
