
from django.forms import ValidationError
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, Trade
from .serializer import OrderSerializer, WalletSerializer, TradeSerializer, TransactionSerializer
from django.db import transaction
import requests
import time
from Apps.Account.models import User, Wallet
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from datetime import datetime, timedelta
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache

class Trading(APIView):
    permission_classes = [AllowAny]

    def __init__(self):
        self.endpoint = "https://api.binance.com/api/v3/klines"
        self.params = {
            "symbol": "BTCUSDT",
            "interval": "1m",
            "limit": 1  # Fetch the latest candlestick
        }
        self.wallet = None

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            order_type = request.data.get('order_type')
            symbol = request.data.get('symbol', 'BTCUSDT')
            price = float(request.data.get('price', 0))

            if order_type not in ["buy", "sell"]:
                return Response({"error": "ประเภทคำสั่งไม่ถูกต้อง"}, status=status.HTTP_400_BAD_REQUEST)

            if price <= 0:
                return Response({"error": "ราคาต้องมากกว่า 0"}, status=status.HTTP_400_BAD_REQUEST)

            # ดึงข้อมูลกระเป๋าเงินของผู้ใช้และตรวจสอบยอดคงเหลือ
            self.wallet = self.get_user_wallet(user)
            if not self.validate_wallet_balance(order_type, price):
                return Response({"error": "ยอดเงินไม่เพียงพอสำหรับคำสั่งนี้"}, status=status.HTTP_400_BAD_REQUEST)

            self.update_wallet(order_type, price)
            self.wallet.save()

            order = Order.objects.create(
                user_id=user,
                order_type=order_type,
                price=price,
                status=Order.STATUS_PENDING,
                symbol=symbol
            )

            # สะสมราคาใน cache
            cache_key = f"trade_{user.id}_price_total"
            trade_data = cache.get(cache_key, {"total_price": 0})
            trade_data["total_price"] += price
            cache.set(cache_key, trade_data)


            last_candle_start = self.fetch_candlestick_data(symbol, 2)
            print("amountprice = ", trade_data["total_price"])
           
            
            
            print("wait for next candleww")
            last_request_cache_key = f"trade_{user.id}_last_request"
            cache.set(last_request_cache_key, {"total_price": trade_data["total_price"] , "symbol": symbol, "order_type": order_type})
            
            
            # รอให้ข้อมูลอัพเดท (เช่น 2 นาที)
            print("wait for next candle")
            self.get_next_candlestick_time()

    
            # ดึงข้อมูลคำขอล่าสุดจาก cache
            last_request = cache.get(last_request_cache_key)

            if last_request:
                total_price = last_request["total_price"]
                symbol = last_request["symbol"]
                order_type = last_request["order_type"]

                # ทำการ execute trade โดยใช้ข้อมูลจากคำขอล่าสุด
                trade_result = self.execute_trade(order_type, symbol, total_price)
                win_or_loss = self.calculate_trade_outcome(order_type, symbol, last_candle_start, total_price)
            else:
                # กรณีที่ไม่มีข้อมูลใน cache
                trade_result = {"error": "ไม่มีข้อมูลคำขอล่าสุดใน cache"}
                win_or_loss = None
            # ทำการ execute trade
            # trade_result = self.execute_trade(order_type, symbol, total_price)
            # win_or_loss = self.calculate_trade_outcome(order_type, symbol, last_candle_start, total_price)

            # อัพเดทสถานะคำสั่ง
            order.status = Order.STATUS_COMPLETED
            order.save()
            



            # บันทึกการเทรดในฐานข้อมูล
            timestamp = timezone.now()
            Trade.objects.create(
                user_id=user,
                trade_type=order_type,
                price=total_price,  # ใช้ total_price แทน amountPrice
                timestamp=timestamp,
                status=Trade.STATUS_COMPLETED,
                symbol=symbol
            )

            # ส่งข้อมูลการเทรดผ่าน WebSocket
            trade_result["win_or_loss"] = win_or_loss

            channel_layer = get_channel_layer()
            cache.set(last_request_cache_key, {"trade_result": trade_result})
            print("trading_buy_sell", {f"user_id {user}, trade_data {trade_result}"})
            async_to_sync(channel_layer.group_send)(
                "trading_buy_sell",
                {
                    'type': 'send_trade_update',
                    'trade_data': trade_result
                }
            )

            cache.delete(cache_key)
            cache.delete(last_request_cache_key)

            return Response(trade_result, status=status.HTTP_200_OK)

        except Exception as e:
            # หากเกิดข้อผิดพลาด
            order.status = "failed"
            order.save()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_user_wallet(self, user):
        if user is None:
            raise ValidationError({"error": "ไม่พบกระเป๋าเงินของผู้ใช้งาน+2"})
        """ดึงข้อมูลกระเป๋าเงินของผู้ใช้"""
        try:
            return Wallet.objects.get(user_id=user)
        except Wallet.DoesNotExist:
            raise ValidationError({"error": "ไม่พบกระเป๋าเงินของผู้ใช้งาน"})
        
        
    def validate_wallet_balance(self, order_type, price):
        """ตรวจสอบว่ายอดเงินในกระเป๋าเพียงพอหรือไม่"""
        if order_type == "buy" and self.wallet.real_balance < price:
            return False
        if order_type == "sell" and self.wallet.real_balance < price:
            return False
        return True
    
    
    def fetch_candlestick_data(self, symbol, start_end):
        """ดึงข้อมูลแท่งเทียนจาก API"""
        start_end = int(start_end)
        self.params["symbol"] = symbol
        response = requests.get(self.endpoint, params=self.params)
        response.raise_for_status()
        data = response.json()
        return float(data[0][start_end])
    
        # try:
        #     candle_start_time = data[0][0]  # สมมติว่าเป็น timestamp ของแท่งเทียน
        #     last_candle_start = datetime.fromtimestamp(candle_start_time / 1000)  # แปลงจาก timestamp (หากจำเป็น)
        # except ValueError as e:
        #     return Response({"error": "ไม่สามารถแปลงข้อมูลแท่งเทียนได้"}, status=status.HTTP_400_BAD_REQUEST)
    
        # return last_candle_start
            
    def wait_for_next_candle(self):
        """รอจนกว่าแท่งเทียนถัดไปจะถูกสร้าง"""
        current_time = int(time.time())
        time_to_wait = 60 - (current_time % 60)
        time.sleep(time_to_wait)
        
    def calculate_trade_outcome(self, order_type, symbol, last_candle_start, price):
        """คำนวณผลว่ากำไร ขาดทุน หรือเท่าทุน"""
        last_candle_close = self.fetch_candlestick_data(symbol,4)  # ดึงข้อมูลล่าสุด
        adjusted_price = price * 1.95  # ปรับกำไร/ขาดทุน
        
        # print("last_candle_close", last_candle_close)
        # print("last_candle_start", last_candle_start)

        if last_candle_close == last_candle_start:
            # print("before--",self.wallet.reserved)
            self.wallet.reserved -= price
            # print("after----",self.wallet.reserved)
            self.wallet.real_balance += price
            self.wallet.save()
            return "equal"

        elif order_type == "buy":
            if last_candle_close > last_candle_start:
                self.wallet.real_balance += adjusted_price
                # print("before", self.wallet.reserved)  # แสดงค่าก่อน
                self.wallet.reserved -= price
                # print("after before save", self.wallet.reserved)  # แสดงค่าหลังการลด
                self.wallet.save()
                self.wallet.refresh_from_db()  # รีเฟรชข้อมูลจากฐานข้อมูล
                # print("after save", self.wallet.reserved)  # แสดงค่าหลังจากการบันทึก
                return f"win = {adjusted_price}"
            else:
                # print("beforeพพพพพพพ222222222222222",self.wallet.reserved)
                self.wallet.reserved -= price
                # print("afteพพพพพพพพr222222",self.wallet.reserved)
                
                self.wallet.save()
                return "lose"

        elif order_type == "sell":
            if last_candle_close < last_candle_start:
                self.wallet.real_balance += adjusted_price
                # print("beforeพพพพพพพ",self.wallet.reserved)
                self.wallet.reserved -= price
                # print("afteพพพพพพพพr",self.wallet.reserved)
                self.wallet.save()
                return f"win = {adjusted_price}"
            else:
                # print("beforeพพพพพพพ222222222222222",self.wallet.reserved)
                self.wallet.reserved -= price
                # print("afteพพพพพพพพr222222",self.wallet.reserved)
                
                self.wallet.save()
                return "lose"
            
    def update_wallet(self, order_type, price):

        self.wallet.reserved += price
        self.wallet.real_balance -= price

        self.wallet.save()
        
    def execute_trade(self, order_type, symbol, price):
        """ทำรายการโดยอัปเดตยอดในกระเป๋าเงินของผู้ใช้"""

        return {
            "order_type": order_type,
            "symbol": symbol,
            "price": price,
            "status": "success",
        }
    
    def get_next_candlestick_time(self):
        try:
            url = 'https://api.binance.com/api/v3/klines'
            params = {
                'symbol': "BTCUSDT", 
                'interval': '1m', 
                'limit': 2,  # Fetch the latest two candlesticks 
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if len(data) < 2:
                print("ข้อมูลแท่งเทียนไม่เพียงพอ", data)
                return

            # Get the second latest candlestick (we need the second one)
            latest_candlestick = data[1]  # Get the second latest candlestick
            latest_timestamp = latest_candlestick[0]

            # Calculate when the second candlestick will be complete
            next_candlestick_time = datetime.utcfromtimestamp(latest_timestamp / 1000) + timedelta(minutes=1)

            # Add an additional minute for the next candlestick
            next_candlestick_time += timedelta(minutes=1)

            current_time = datetime.utcnow()
            time_diff = next_candlestick_time - current_time
            seconds_remaining = int(time_diff.total_seconds())

            if seconds_remaining > 0:
                minutes_remaining = seconds_remaining // 60
                seconds_only = seconds_remaining % 60
                print(f"แท่งเทียนถัดไปจะเสร็จใน {minutes_remaining} นาทีและ {seconds_only} วินาที")
                time.sleep(seconds_remaining)  # Wait for the second candlestick to complete
            else:
                print("The next candlestick time has already passed.")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching candlestick data: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    

class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()  
    serializer_class = WalletSerializer  
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        """
        ปรับแต่ง queryset เพื่อรองรับการกรองข้อมูลกระเป๋าเงินเฉพาะผู้ใช้งาน 
        หรือดึงข้อมูลกระเป๋าเงินทั้งหมด
        """
        
        user = self.request.user  # ดึงข้อมูลผู้ใช้ที่ผ่านการยืนยันตัวตน
        user_only = self.request.query_params.get('user_only', 'true').lower() == 'true'  # ตรวจสอบว่า user_only มีค่า true หรือไม่

        if user_only:
            # ดึงกระเป๋าเงินที่เกี่ยวข้องกับผู้ใช้ปัจจุบันเท่านั้น
            return Wallet.objects.filter(user_id=user)
        
        # ดึงกระเป๋าเงินทั้งหมด หากไม่ได้ระบุ user_only หรือระบุค่าเป็น false
        return Wallet.objects.all()
    
    
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()  
    serializer_class = TransactionSerializer  
    permission_classes = [IsAuthenticated]
    


