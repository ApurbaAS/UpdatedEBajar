from django.db import models
from .categorys import Category
import locale


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    product_des = models.TextField(max_length=500, default='', null=True, blank=True)
    product_img = models.ImageField(upload_to='upload/product_imgage/')
    
    
    @property
    def formatted_price(self):
        locale.setlocale(locale.LC_MONETARY, 'en_IN')
        format_price = locale.currency(self.price, grouping=True)
        return format_price
        
    
    
    def __str__(self) -> str:
        return self.name
    
    #Getting All Products From the Database, 
    #we need Static Method for that
    @staticmethod
    def get_products():
        return Product.objects.all()
    
    
    @staticmethod
    def get_product_by_id(id_list):
        return Product.objects.filter(id__in = id_list)
    
    
    
    @staticmethod
    def products_by_cat_id(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_products()
    