import redis

from django.conf import settings

from .models import Product


r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


class Recommender:

    def get_product_key(self, pk):
        return f'product:{pk}:purchased_with'

    def products_bought(self, order):
        products = list(order.order_items.all())
        for product_item in products:
            for with_item in products:
                if with_item != product_item:
                    r.zincrby(self.get_product_key(product_item.product.pk),
                              product_item.quantity,
                              with_item.product.pk)

    def suggest_products_for(self, products, max_results=6):
        product_pks = [p.pk for p in products]
        if len(products) == 1:
            suggestions = r.zrange(self.get_product_key(product_pks[0]),
                                   0,
                                   max_results-1,
                                   desc=True)
        else:
            flat_ids = ','.join([str(pk) for pk in product_pks])
            tmp_key = f'tmp_{flat_ids}'
            keys = [self.get_product_key(pk) for pk in product_pks]
            r.zunionstore(tmp_key, keys)
            r.zrem(tmp_key, *product_pks)
            suggestions = r.zrange(tmp_key, 0, max_results-1, desc=True)
            r.delete(tmp_key)

        suggested_product_pks = [int(pk) for pk in suggestions]
        suggested_products = list(Product.objects.filter(pk__in=suggested_product_pks))
        suggested_products.sort(key=lambda x: suggested_product_pks.index(x.pk))
        return suggested_products
