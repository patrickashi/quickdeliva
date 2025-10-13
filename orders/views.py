from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save order
        order = serializer.save(user=self.request.user)

        # ✅ Compose admin email with order details
        subject = f"New Quickdeliva Order from {order.user.email}"
        message = (
            f"📦 A new order has been placed on Quickdeliva 🚚\n\n"
            f"Customer: {order.user.username} ({order.user.email})\n"
            f"Phone: {order.user.phone_number}\n"
            f"Pickup Address: {order.pickup_address}\n"
            f"Delivery Address: {order.delivery_address}\n"
            f"Package Description: {order.package_description}\n"
            f"Preferred Vehicle: {order.preferred_vehicle}\n"
            f"Delivery Date: {order.delivery_date}\n"
            f"Delivery Time: {order.delivery_time}\n"
            f"Special Instructions: {order.special_instructions or 'None'}\n\n"
            f"Order Status: {order.status}\n"
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],  # <-- make sure ADMIN_EMAIL is set in settings.py
            fail_silently=False,
        )


class OrderStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Always return order counts grouped by month (even if user has only 1 order).
        """
        stats = (
            Order.objects.filter(user=request.user)
            .annotate(order_month=TruncMonth("created_at"))
            .values("order_month")
            .annotate(total=Count("id"))
            .order_by("order_month")
        )

        results = []
        for row in stats:
            month_display = row["order_month"].strftime("%b %Y") if row["order_month"] else "Unknown"
            results.append({
                "month": month_display,
                "total": row["total"],
            })

        return Response(results)
    