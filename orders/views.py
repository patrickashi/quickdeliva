from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.core.mail import send_mail
from django.conf import settings
from .models import Order
from .serializers import OrderSerializer
import calendar


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save the order first
        order = serializer.save(user=self.request.user)

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
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )


class OrderStatsView(APIView):
    """
    Returns monthly order counts for the current user.
    Ensures the frontend always receives chart-friendly data.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # Group orders by creation month
        stats = (
            Order.objects.filter(user=user)
            .annotate(order_month=TruncMonth("created_at"))
            .values("order_month")
            .annotate(total=Count("id"))
            .order_by("order_month")
        )

        results = []
        for row in stats:
            # Defensive month name conversion
            if row["order_month"]:
                month_name = calendar.month_abbr[row["order_month"].month]
                year = row["order_month"].year
                label = f"{month_name} {year}"
            else:
                label = "Unknown"

            results.append({"month": label, "total": row["total"]})

        # ✅ Ensure frontend always receives something
        if not results:
            results = [{"month": "No Orders Yet", "total": 0}]

        # ✅ Recharts really needs numeric 'total'
        results = [
            {"month": r["month"], "total": int(r.get("total", 0))} for r in results
        ]

        return Response(results)