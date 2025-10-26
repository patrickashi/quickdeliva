from django.urls import path
from .views import RegisterView, VerifyEmailView, ProfileView, AvailableDriversView, DashboardView, CustomLoginView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import PasswordResetRequestView, PasswordResetConfirmView
from .views import ContactMessageCreateView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verify/", VerifyEmailView.as_view()),
    path("login/", CustomLoginView.as_view()),   # ✅ supports username OR email
    path("refresh/", TokenRefreshView.as_view()),
    path("me/", ProfileView.as_view()),
    path("drivers/available/", AvailableDriversView.as_view()),
    path("dashboard/", DashboardView.as_view()),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password-reset"),
    path("password-reset-confirm/", PasswordResetConfirmView.as_view()),
    path("contact/", ContactMessageCreateView.as_view(), name="contact-message"),
]