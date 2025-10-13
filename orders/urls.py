from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderStatsView

router = DefaultRouter()
router.register(r"", OrderViewSet, basename="orders")

urlpatterns = router.urls + [
    path("stats/", OrderStatsView.as_view(), name="order-stats"),
]