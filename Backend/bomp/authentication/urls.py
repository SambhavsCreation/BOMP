from django.urls import path

from .views import (
    ConfirmEnable2FAView,
    Enable2FAView,
    LoginView,
    RegisterView,
    TwoFALoginView,
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("login/2fa/", TwoFALoginView.as_view()),
    path("2fa/enable/", Enable2FAView.as_view()),
    path("2fa/confirm/", ConfirmEnable2FAView.as_view()),
]
