from django.urls import path

from . import views


app_name = 'order'

urlpatterns = [
    path('create/', views.order_view, name='create'),
    path('payment/<int:pk>', views.payment_view, name='payment'),
    path('complete/<int:pk>', views.complete_view, name='complete'),
    path('invoice/<int:pk>', views.invoice_view, name='invoice'),
]
