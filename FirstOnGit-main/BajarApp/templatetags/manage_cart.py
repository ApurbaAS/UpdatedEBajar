import locale
from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    keys = cart.keys()

    for id in keys:
        if int(id) == product.id:
            return True
    return False

@register.filter(name='cart_count')
def cart_count(product  , cart):
    keys = cart.keys()
    
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)

    return 0



@register.filter(name='cart_amount')    
def cart_amount(product, cart):
    total = product.price * cart_count(product, cart)
    locale.setlocale(locale.LC_MONETARY, 'en_IN')
    formatted_total = locale.currency(total, grouping=True)
    return formatted_total



@register.filter(name='total_cart_price')
def total_cart_price(products, cart):
    sum = 0
    for p in products:
        formatted_amount = cart_amount(p, cart).replace(',', '').replace('₹', '')
        sum += int(float(formatted_amount))
    
    locale.setlocale(locale.LC_MONETARY, 'en_IN')
    formatted_sum = locale.currency(sum, grouping=True)
    return formatted_sum

