from django.urls import path
from .views import KlineDataView

urlpatterns = [
    path('klines/', KlineDataView.as_view(), name='kline-data'),
]