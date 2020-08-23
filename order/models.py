from django.db import models

from shop.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=20)
    paid = models.BooleanField(default=False)
    payment_time = models.DateTimeField(blank=True,
                                        null=True)

    def __str__(self):
        return f'Order #{self.pk}'

    def get_total_price(self):
        return sum(item.get_cost() for item in self.order_items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    quantity = models.IntegerField()

    def get_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.quantity}x {self.product.name} for Order #{self.order.pk}'
