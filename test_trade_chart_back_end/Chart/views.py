# Chart/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class KlineDataView(APIView):
    def get(self, request):
        # Fetch data from Binance API
        endpoint = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": "BTCUSDT",
            "interval": "1m",
            "limit": 1000
        }
        response = requests.get(endpoint, params=params)
        data = response.json()

        # Process the data for chart display
        processed_data = [
            {
                "time": int(d[0] / 1000),
                "open": float(d[1]),
                "high": float(d[2]),
                "low": float(d[3]),
                "close": float(d[4])
            }
            for d in data
        ]

        # Send data to WebSocket group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'ws_klines',  # Group name must match the consumer
            {
                'type': 'send_kline_data',  # Custom type to trigger a specific function in consumer
                'data': processed_data
            }
        )

        return Response(processed_data)
