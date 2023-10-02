import locale
from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(number1, number2):
    formatted_amount = number2.replace(',', '').replace('₹', '')
    
    # # Convert formatted_amount and number2 to float or int
    # formatted_amount = float(formatted_amount)
    # number2 = float(number2)

    formatted_amount = float(formatted_amount)

    total = number1 * formatted_amount
    
    locale.setlocale(locale.LC_MONETARY, 'en_IN')
    formatted_sum = locale.currency(total, grouping=True)
    return formatted_sum

