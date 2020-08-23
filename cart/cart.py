from decimal import Decimal
from django.conf import settings

from shop.models import Product


class Cart:

    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(settings.SESSION_CART_ID)
        if not self.cart:
            self.cart = self.session[settings.SESSION_CART_ID] = {}

    def add(self, product, quantity, override=True):
        product_pk = str(product.pk)
        if product_pk not in self.cart:
            self.cart[product_pk] = {'quantity': 0,
                                     'price': str(product.price)}
        if override:
            self.cart[product_pk]['quantity'] = quantity
        else:
            self.cart[product_pk]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_pk = str(product.pk)
        if product_pk in self.cart:
            del self.cart[product_pk]
        self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        if self.session and self.cart:
            del self.session[settings.SESSION_CART_ID]

    def get_total_price(self):
        return sum(Decimal(x['price']) * x['quantity'] for x in self.cart.values())

    def __len__(self):
        return sum(x['quantity'] for x in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(pk__in=product_ids)

        for product in products:
            item = self.cart.get(str(product.pk)).copy()
            item['product'] = product
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
