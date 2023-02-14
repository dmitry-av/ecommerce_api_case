"""stripeApp URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
import purchase.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("purchase.api.urls")),
]
