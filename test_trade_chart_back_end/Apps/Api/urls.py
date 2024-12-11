from django.urls import path
from Apps.Chart.views import (KlineDataView, TradeView, TimeUntilNextCandlestickView)
from Apps.Account.views import (
    UserLoginView,
    UserRegisterCreateAPIview,
    UserViewsets,
    GroupViewSet,
    GroupViewSet,
    PermissionViewSet,
    User_Me,
    VerifyEmailAPIView,
    ResendVerificationEmailAPIView)
from .views import LIstApiAPIview
from rest_framework.routers import DefaultRouter
from Apps.Trading.views import (Trading, WalletViewSet)


app_name = "api"
router = DefaultRouter()

# router.register(r"get-user", UserDetailViews, basename="get_user")
router.register(r"user", UserViewsets, basename="user")
router.register(r"group", GroupViewSet, basename="group")
router.register(r"permission", PermissionViewSet, basename="permission")
router.register(r"wallet", WalletViewSet, basename="wallet")
# router.register(r'wallets', WalletViewSet, basename="wallet")


urlpatterns = [
    path("", LIstApiAPIview.as_view(), name="list_api_view"),
    path('klines/', KlineDataView.as_view(), name='kline-data'),
    path('trade/', TradeView.as_view(), name='trade'),
    path("auth-me/", User_Me.as_view(), name="auth-me"),
    path('user-login/', UserLoginView.as_view(), name='user_login'),
    path('time_until_next_candlestick/', TimeUntilNextCandlestickView.as_view(), name='time_until_next_candlestick'),
    path('user-register/', UserRegisterCreateAPIview.as_view(), name='user_register'),
    path('trading/', Trading.as_view(), name='trading'),
    path("verify-email/", VerifyEmailAPIView.as_view(), name="verify-email"),
    path("resend-verify-email/", ResendVerificationEmailAPIView.as_view(), name="resend-verify-email"),
    # path('users/', UserDetailAPIView.as_view(), name='user-list'),  # Get all users
    # path('users/<int:id>/', UserDetailAPIView.as_view(), name='user-detail'),  # Get user by ID
    # path('users/<int:id>/', UserDetailAPIView.as_view(), name='user-detail'),
]

urlpatterns += router.urls