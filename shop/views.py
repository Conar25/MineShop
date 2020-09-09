import redis

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.conf import settings

from .models import Category, Product
from .recommender import Recommender
from .utils import is_ajax


r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


def list_view(request, slug=None):
    categories = Category.objects.all()
    products = Product.objects.all()
    active_category = None
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = category.products.all()
        active_category = category.name
    # Popular products
    product_ranking = r.zrange('product_ranking', 0, 4, desc=True)
    product_pks = [int(pk) for pk in product_ranking]
    popular_products = list(Product.objects.filter(pk__in=product_pks))
    popular_products.sort(key=lambda x: product_pks.index(x.pk))

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
                   'active_category': active_category,
                   'popular_products': popular_products})


def detail_view(request, slug, pk):
    product = get_object_or_404(Product, pk=pk, slug=slug)

    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    recommended_products = None

    return render(request, 'shop/detail.html',
                  {'product': product,
                   'recommended_products': recommended_products})
