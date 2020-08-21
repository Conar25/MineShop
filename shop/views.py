from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse

from .models import Category, Product
from .utils import is_ajax


def list_view(request, slug=None):
    categories = Category.objects.all()
    products = Product.objects.all()
    active_category = None
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = category.products.all()
        active_category = category.name
    # Pagination
    paginator = Paginator(products, 5)
    page_number = int(request.GET.get('page', 1))
    if page_number > paginator.num_pages:
        return HttpResponse('')
    products = paginator.get_page(page_number)
    if is_ajax(request):
        return render(request, 'shop/products_ajax.html', {'products': products})
    return render(request, 'shop/list.html',
                  {'categories': categories,
                   'products': products,
                   'active_category': active_category})


def detail_view(request, slug, pk):
    product = get_object_or_404(Product, pk=pk, slug=slug)
    return render(request, 'shop/detail.html',
                  {'product': product})
