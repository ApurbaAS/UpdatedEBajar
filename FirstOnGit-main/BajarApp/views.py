from django.views import View
from django.contrib import messages
from .models import categorys, products, user_clients, orders
from BajarApp.models.user_clients import User_Client
from .forms import UserClientForm
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect, HttpResponseRedirect
from BajarApp.middleware.auth import simple_middleware

# Create your views here.

class Home(View):
    def get(self, request):
        
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        
        category = categorys.Category.get_categories()
        category_id = request.GET.get('category')
        product = None
        if category_id:
            product = products.Product.products_by_cat_id(category_id)
        else:
            product = products.Product.get_products()
        data = {
            'products': product,
            'categorys': category,
        }
        return render(request, 'index.html', data) 

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            print('its already have')
            qty = cart.get(product)
            if qty:
                if remove:
                    if qty <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = qty-1
                else:
                    cart[product] = qty+1
            else:
                cart[product] = 1
            print(cart)
        else:
            print('its dont have')
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart  
        
        return redirect('home')
    

class RegisterUser(View):
    def get(self, request):
        form = UserClientForm(request=request)
        return render(request, 'register_user.html', {'form': form})
    def post(self, request):
        form = UserClientForm(request.POST, request=request)  # Pass the request object to the form
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])  # Hash the password
            
            user.save()
            user.send_verification_email(request)
            return redirect('home')
        else:
            return render(request, 'register_user.html', {'form': form})
        
        
class LoginUser(View):
    return_url = ''
    def get(self, request):
        LoginUser.return_url = request.GET.get('return_url')
        return render(request, 'login.html', {'login_messages': messages.get_messages(request)})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_client = user_clients.User_Client.get_user_email(email)
        
        if user_client:
            pas = check_password(password, user_client.password)
            if pas:
                
                request.session['user_id'] = user_client.id
                request.session['email'] = user_client.email
                
                if LoginUser.return_url:
                    return HttpResponseRedirect(LoginUser.return_url)
                else:
                    LoginUser.return_url = ''
                    return redirect('home')
            else:
                messages.error(request, 'Invalid Email or Password, Try again!') 
        else:
            messages.error(request, 'Invalid Email or Password, Try again!') 
            
            
        return render(request, 'login.html', {'login_messages': messages.get_messages(request)})
    
    def logout(request):
        request.session.clear()
        messages.error(request, 'You are Logged Out!') 
        return redirect('login')
    

class Cart(View):
    def get(self, request):
        user = request.session.get('email')
        if user:
            id_list = list(request.session.get('cart').keys())
            cart_products = products.Product.get_product_by_id(id_list)
            print(f"This is CartProducts: {cart_products}")
            return render(request, 'cart_page.html', {'cart_products': cart_products})
        else:
            return redirect('login')
    
class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('user_id')
        cart = request.session.get('cart')
        products_id = products.Product.get_product_by_id(list(cart.keys()))
        print(f"Customer: {customer}, Cart: {cart}, Product: {products_id}")
        
        
        for product in products_id:
            print(f"This is Product ID {cart.get(str(product.id))}")
            order = orders.Order(customer=User_Client(id =customer), product=product, price=product.price, quantity=cart.get(str(product.id)), address=address, phone=phone)
            
            order.save()
        
        request.session['cart'] = {}
            
        return redirect('cart')


class Orders(View):
    @method_decorator(simple_middleware)
    def get(self, request):
        customer = request.session.get('user_id')
        orders_view = orders.Order.get_orders_by_customer(customer)
        
        
        
        return render(request, 'orders.html', {'orders_view':orders_view})
    
    
    
    
    
    