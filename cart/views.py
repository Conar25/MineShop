from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from shop.models import Product
from shop.recommender import Recommender

from .cart import Cart


@require_POST
def add_view(request, pk):
    quantity = int(request.POST.get('quantity', default=1))
    override = False if request.POST.get('override') == "False" else True
    product = get_object_or_404(Product, pk=pk)

    cart = Cart(request)
    cart.add(product, quantity, override=override)
    return redirect('cart:cart')


@require_POST
def remove_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    cart = Cart(request)
    cart.remove(product)
    return redirect('cart:cart')


def cart_view(request):
    cart = Cart(request)
    products = [item['product'] for item in cart]
    if products:
        r = Recommender()
        recommended_products = r.suggest_products_for(products)
    else:
        recommended_products = None
    return render(request, 'cart/cart.html',
                  {'recommended_products': recommended_products})
