from django.urls import path
from orders.views import OrderAPIView

urlpatterns = [
    path("orders/", OrderAPIView.as_view(), name="order-create"),
    path("orders/<uuid:order_id>/", OrderAPIView.as_view(), name="order-detail"),
]
