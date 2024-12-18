import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from binance.client import Client
from binance.streams import BinanceSocketManager
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime, timedelta
import requests
from channels.db import database_sync_to_async
from django.apps import apps


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
            
  
import json
# import httpx


# class CandlestickConsumer(AsyncWebsocketConsumer):
    
#     async def connect(self):
#         print("WebSocket Connected!")
#         self.room_name = "candlestick_room"
#         self.room_group_name = f"candlestick_{self.room_name}"

#         # Join the group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def send_next_candlestick_time(self):
#         # ดึงข้อมูลแท่งเทียนจาก Binance API
#         try:
#             url = 'https://api.binance.com/api/v3/klines'
#             params = {
#                 'symbol': "BTCUSDT",
#                 'interval': '1m',
#                 'limit': 1,  # ดึงแค่แท่งเทียนล่าสุด
#             }

#             # ใช้ httpx แทน requests
#             async with httpx.AsyncClient() as client:
#                 response = await client.get(url, params=params)

#             response.raise_for_status()  # ตรวจสอบข้อผิดพลาด
#             data = response.json()
#             print(f"Received data: {data}")

#             if not data:
#                 raise ValueError("No data found for this symbol")

#             latest_candlestick = data[0]
#             latest_timestamp = latest_candlestick[0]  # timestamp ของแท่งเทียนล่าสุด
#             next_candlestick_time = datetime.utcfromtimestamp(latest_timestamp / 1000) + timedelta(minutes=1)

#             # คำนวณจำนวน นาที่ที่เหลือ
#             now = datetime.utcnow()
#             time_diff = next_candlestick_time - now
#             minutes_remaining = int(time_diff.total_seconds() // 60)  # แปลงเวลาที่เหลือเป็นนาที

#             # ส่งข้อมูลเวลาแท่งเทียนถัดไปและนาทีที่เหลือ
#             await self.send(text_data=json.dumps({
#                 'next_candlestick_time': next_candlestick_time.isoformat(),
#                 'minutes_remaining': minutes_remaining
#             }))

#         except httpx.RequestError as e:
#             await self.send(text_data=json.dumps({
#                 'error': f'Failed to get data: {str(e)}'
#             }))
#         except ValueError as e:
#             await self.send(text_data=json.dumps({
#                 'error': str(e)
#             }))

#     async def receive(self, text_data):
#         # รับคำขอจาก frontend ให้ส่งข้อมูลแท่งเทียนถัดไป
#         data = json.loads(text_data)

#         if data.get('request_next_candlestick_time'):
#             await self.send_next_candlestick_time()


class WalletConsumer(AsyncWebsocketConsumer):
        
    async def connect(self):
        self.room_group_name = "wallet_update"

        # เข้าร่วมกลุ่ม WebSocket
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print("WebSocket joining done ...!")

    async def disconnect(self, close_code):
        # ออกจากกลุ่ม WebSocket
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # รับข้อมูลจาก WebSocket (ถ้ามี)
        text_data_json = json.loads(text_data)
        action = text_data_json.get("action", None)

        # ถ้าต้องการให้เช็คหรือรับข้อมูลจาก WebSocket
        if action == "fetch_wallet":
            wallet_data = await self.get_wallet_data()
            await self.send(text_data=json.dumps({
                "wallet": wallet_data
            }))

    @database_sync_to_async
    def get_wallet_data(self):
        self.Wallet = apps.get_model('Account', 'Wallet')
       
        # ดึงข้อมูลจากฐานข้อมูล
        wallet = self.Wallet.objects.first()  # ดึงข้อมูล wallet ตัวแรก
        print(f"Wallet data: {wallet.real_balance}, {wallet.demo_balance}")  # พิมพ์ข้อมูล
        return {
            "real_balance": wallet.real_balance,
            "demo_balance": wallet.demo_balance
        }

    async def send_wallet_update(self, event):
        print("sending to ...")
        # ส่งการอัปเดตข้อมูลไปยัง WebSocket
        print("Event data:", event['wallet'])
        await self.send(text_data=json.dumps({
            "wallet": event['wallet']
        }))
        print("send to done...")
        
        



class TradingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "buy_sell"
        self.room_group_name = f'trading_{self.room_name}'
        print(f"Connecting to room: {self.room_group_name}")

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print(f"Disconnecting from room: {self.room_group_name}")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(f"Received message: {text_data}")
        data = json.loads(text_data)
        order_type = data.get('order_type')
        price = data.get('price')
        symbol = data.get('symbol')

        # Process order logic (you can call the trading logic here)
        # For example, simulate trade execution:
        response = {
        'status': 'success',
        'order_type': order_type,
        'price': price,
        'symbol': symbol,
        "win_or_loss":"equal"
        }

    # Send response to WebSocket
        await self.send(text_data=json.dumps(response))  # Corrected json.dumps() syntax


    # Send message to WebSocket
    async def send_trade_update(self, event):
        trade_data = event['trade_data']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(trade_data))
        
