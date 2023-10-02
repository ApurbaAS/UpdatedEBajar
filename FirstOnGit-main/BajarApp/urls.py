from django.urls import path
from . import views
from .views import LoginUser
from .middleware.auth import simple_middleware

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('check_out', views.CheckOut.as_view(), name='check_out'),
    path('orders', simple_middleware(views.Orders.as_view()), name='orders'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LoginUser.logout, name='logout'),
    
]
