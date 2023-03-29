from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from rest_framework.authtoken.views import obtain_auth_token


router = routers.DefaultRouter()

router.register("orders", views.OrderViewSet)


order_router = routers.NestedDefaultRouter(router, "orders", lookup="order")
order_router.register("items", views.OrderItemViewSet, basename="order-items")


urlpatterns = [
    path("", include(router.urls), name='orders'),
    path("", include(order_router.urls)),
    path('get-details', views.UserDetailAPI.as_view()),
    path('register', views.RegisterUserAPIView.as_view()),
    path("item/<int:pk>", views.ItemDetail.as_view(), name='item-detail'),
    path("order/<pk>", views.OrderDetail.as_view(), name='order-detail'),
    path("checkout-session/<pk>/", views.CreateCheckoutSessionView.as_view(),
         name="create-checkout-session"),
    path("order-checkout-session/<pk>/", views.OrderCheckoutSessionView.as_view(),
         name="order-checkout-session"),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
    path('success/', views.SuccessView.as_view(), name='success'),
]

urlpatterns += [path('api-token-auth', obtain_auth_token),
                path('auth/', include('rest_framework.urls'))
                ]
