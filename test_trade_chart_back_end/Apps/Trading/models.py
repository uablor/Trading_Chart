from django.db import models
from Apps.Account.models import User, Wallet  # Assuming you're using the built-in User model
from Common.models.base_models import Base_model
    
class Order(Base_model):
    TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]
    
    STATUS_PENDING = 'pending'
    STATUS_COMPLETED = 'completed'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETED, 'Completed')
    ]
    
    user_id = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    order_type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False, null=False)
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)  # auto_now_add=True will set the date when the order is created
    status = models.CharField(max_length=20, blank=False,choices=STATUS_CHOICES, null=False)
    symbol = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return f"Order {self.id} - {self.order_type} - {self.price}"
    

class Trade(Base_model):
    TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]
    
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    trade_type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False, null=False)
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=False, null=False)
    timestamp = models.DateTimeField(blank=False, null=False)  # store exact timestamp for the trade
    user_id = models.ForeignKey(User, related_name='trades', on_delete=models.CASCADE)
    symbol = models.CharField(max_length=200, blank=False, null=False)
    def __str__(self):
        return f"Trade {self.id} - {self.trade_type} - {self.price} - {self.status}"
    
    
class Transaction(Base_model):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES, blank=False, null=False)
    user_id = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False)
    transaction_date = models.DateTimeField(blank=False, null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=False, null=False)

    def __str__(self):
        return f"Transaction {self.id} - {self.transaction_type} - {self.amount} - {self.status}"