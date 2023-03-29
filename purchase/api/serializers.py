from rest_framework import serializers
from django.contrib.auth.models import User
from purchase.models import Item, Order, OrderItem
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username"]


# Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


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
        fields = ["id", "creator", "items", "grand_total"]
        read_only_fields = [
            "creator",
        ]

    def main_total(self, cart: Order):
        items = cart.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total
