import locale
from django.db import models
from datetime import datetime
from .user_clients import User_Client
from .products import Product

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User_Client, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    phone = models.CharField(max_length=15, default="", blank=True)
    address = models.CharField(max_length=400, default="", blank=True)
    date = models.DateField(default=datetime.today)
    status = models.BooleanField(default=False)

    
    
    @property
    def formatted_order_price(self):
        locale.setlocale(locale.LC_MONETARY, 'en_IN')
        format_price = locale.currency(self.price, grouping=True)
        return format_price
    
    def formatted_date(self):
        return self.date.strftime("%d/%m/%Y")

    def __str__(self):
        return f"{self.customer} - {self.product.name} - {self.status}"
    
    
    
    
    
    def placeOrder(self):
        self.save()
        
    @staticmethod
    def get_orders_by_customer(user_id):
        return Order.objects.filter(customer = user_id).order_by('-date', '-id')