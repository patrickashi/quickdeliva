from django.urls import path
from .views import RegisterView, VerifyEmailView, ProfileView, AvailableDriversView, DashboardView, CustomLoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verify/", VerifyEmailView.as_view()),
    path("login/", CustomLoginView.as_view()),   # ✅ supports username OR email
    path("refresh/", TokenRefreshView.as_view()),
    path("me/", ProfileView.as_view()),
    path("drivers/available/", AvailableDriversView.as_view()),
    path("dashboard/", DashboardView.as_view()),
]