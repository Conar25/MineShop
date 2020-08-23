from django.urls import path

from . import views


app_name = 'cart'

urlpatterns = [
    path('add/<int:pk>', views.add_view, name='add'),
    path('remove/<int:pk>', views.remove_view, name='remove'),
    path('', views.cart_view, name='cart'),
]
