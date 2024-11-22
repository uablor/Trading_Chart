from django.urls import path
from .views import (KlineDataView, TradeView, TimeUntilNextCandlestickView)


urlpatterns = [
    path('klines/', KlineDataView.as_view(), name='kline-data'),
    path('trade/', TradeView.as_view(), name='trade'),
    path('time_until_next_candlestick/', TimeUntilNextCandlestickView.as_view(), name='time_until_next_candlestick'),
]