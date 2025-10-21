from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderStatsView

router = DefaultRouter()
router.register(r"", OrderViewSet, basename="orders")

urlpatterns = [
    # custom non‑model routes must come *before* including the router
    path("stats/", OrderStatsView.as_view(), name="order-stats"),

    # router's model‑based endpoints (/orders/, /orders/{id}/)
    path("", include(router.urls)),
]