import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Item(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=60)
    description = models.TextField()
    stripe_product_id = models.CharField(max_length=100)
    stripe_price_id = models.CharField(max_length=100)
    currency = models.CharField(max_length=5)
    price = models.PositiveIntegerField(null=True)  # in cents

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def main_total(self):
        items = self.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total/100

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(
        Item, on_delete=models.SET_NULL, null=True, related_name='orderitem')
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, related_name="items")
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)

    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return f"Order {self.order.id}, {self.product.name} {self.quantity} ea."
