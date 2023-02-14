from django.contrib import admin
from purchase.models import Item, Order, OrderItem

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
