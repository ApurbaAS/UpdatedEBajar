from django.contrib import admin
from .models.products import Product
from django.template.defaultfilters import linebreaksbr
from .models.categorys import Category
from .models.user_clients import User_Client
from .models.orders import Order

# admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(User_Client)

# @admin.register(Product)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'formatted_product_des')

    def formatted_product_des(self, obj):
        return linebreaksbr(obj.product_des)
    formatted_product_des.short_description = 'Product Description'
    
    
# class UserClientAdmin(admin.ModelAdmin):
#     readonly_fields = ('password')
    
    
admin.site.register(Order)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(User_Client)
    
    
    