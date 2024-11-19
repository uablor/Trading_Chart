import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from binance.client import Client
from binance.streams import BinanceSocketManager
from channels.layers import get_channel_layer

class KlineConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'klines'
        self.room_group_name = f'ws_{self.room_name}'
        
        # Join WebSocket group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # Accept WebSocket connection
        await self.accept()
        
        # Initialize Binance API client
        self.client = Client(api_key='', api_secret='')
        
        # Initialize BinanceSocketManager
        self.bsm = BinanceSocketManager(self.client)
        
        # Start Kline Stream (BTC/USDT 1m)
        self.socket = self.bsm.kline_socket('BTCUSDT', interval='1m')
        
        # Run WebSocket stream in background
        asyncio.create_task(self.run_socket())

    async def run_socket(self):
        try:
            async with self.socket as socket_manager:
                while True:
                    message = await socket_manager.recv()
                    if message:
                        await self.handle_kline_data(message)
        except Exception as e:
            print(f"Error in run_socket: {e}")
            await self.close()

    async def disconnect(self, close_code):
        # Leave WebSocket group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        # Stop Kline Stream
        if hasattr(self, 'socket'):
        # Close the socket if necessary (this may depend on the library version)
            try:
                await self.socket.close()  # If the socket has this method
            except AttributeError:
            # If the socket does not have the close method, just pass
                pass

    async def handle_kline_data(self, data):
        try:
            kline = data.get('k', {})  # Binance sends kline data in 'k' key
            kline_data = {
                'time': kline.get('t', 0) // 1000,  # Convert to seconds
                'open': float(kline.get('o', 0)),
                'high': float(kline.get('h', 0)),
                'low': float(kline.get('l', 0)),
                'close': float(kline.get('c', 0))
            }
            
            await self.send_kline_data_to_group(kline_data)
        except Exception as e:
            print(f"Error processing kline data: {e}")

    async def send_kline_data(self, event):
        # This method is called when group_send is called
        try:
            await self.send(text_data=json.dumps({
                'klines': event['data']
            }))
        except Exception as e:
            print(f"Error sending kline data: {e}")

    async def send_kline_data_to_group(self, data):
        try:
            channel_layer = get_channel_layer()
            await channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_kline_data',
                    'data': data
                }
            )
        except Exception as e:
            print(f"Error sending to group: {e}")