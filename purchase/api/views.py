import stripe
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from rest_framework.views import APIView
from django.views import View
from django.views.generic import TemplateView
from django.conf import settings
import os

from purchase.api.serializers import OrderItemSerializer, AddOrderItemSerializer, OrderSerializer
from purchase.models import Item, Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


class ItemDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'purchase/item_detail.html'

    def get(self, request, pk, format=None):
        item = get_object_or_404(Item, id=pk)
        return Response({'item': item})


class OrderDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'purchase/order_detail.html'

    def get(self, request, pk, format=None):
        order = get_object_or_404(Order, id=pk)
        return Response({'order': order})


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(ModelViewSet):
    def get_queryset(self):
        return OrderItem.objects.filter(order_id=self.kwargs["order_pk"])

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddOrderItemSerializer

        return OrderItemSerializer

    def get_serializer_context(self):
        return {"order_id": self.kwargs["order_pk"]}


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        item = Item.objects.get(id=self.kwargs["pk"])
        domain = os.environ.get("CURRENT_DOMAIN")
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': item.stripe_price_id,
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )
        return redirect(checkout_session.url)


class OrderCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        order = Order.objects.get(id=self.kwargs["pk"])
        domain = os.environ.get("CURRENT_DOMAIN")
        line_items = []
        for item in order.items.all():
            line_items.append(
                {"price": item.product.stripe_price_id, "quantity": item.quantity})
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )
        return redirect(checkout_session.url)


class SuccessView(TemplateView):
    template_name = "purchase/success.html"


class CancelView(TemplateView):
    template_name = "purchase/cancel.html"
