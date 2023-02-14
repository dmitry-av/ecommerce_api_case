from rest_framework import serializers
from purchase.models import Item, Order, OrderItem


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name", "description", "price"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = ItemSerializer(many=False)
    sub_total = serializers.SerializerMethodField(method_name="total")

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity", "sub_total"]

    def total(self, cartitem: OrderItem):
        return cartitem.quantity * cartitem.product.price


class AddOrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()

    def validate_product_id(self, value):
        if not Item.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                "There is no product associated with the given ID")

        return value

    def save(self, **kwargs):
        order_id = self.context["order_id"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        try:
            orderitem = OrderItem.objects.get(
                product_id=product_id, order_id=order_id)
            orderitem.quantity += quantity
            orderitem.save()

            self.instance = orderitem

        except:

            self.instance = OrderItem.objects.create(
                order_id=order_id, **self.validated_data)

        return self.instance

    class Meta:
        model = OrderItem
        fields = ["id", "product_id", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField(method_name='main_total')

    class Meta:
        model = Order
        fields = ["id", "items", "grand_total"]

    def main_total(self, cart: Order):
        items = cart.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total
