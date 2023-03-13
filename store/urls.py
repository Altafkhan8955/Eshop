from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
#from .views.home import index
from .views import signup
from .views import login
from .views import index
from .views import cart
from .views import checkout
from .views import Orderview
from .import views
from store.middlewares.auth import auth_middleware


urlpatterns = [
    path('',index.as_view(),name='index'),
    path('signup',signup.as_view(),name='signup'),
    path('login',login.as_view(),name="login"),
    path('logout',views.logout,name='logout'),
    path('cart',cart.as_view(),name='cart'),
    path('checkout',checkout.as_view(),name='checkout'),
    path('Orderview',Orderview.as_view(),name='Orderview')
    
]
