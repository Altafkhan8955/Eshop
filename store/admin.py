from django.contrib import admin
from .models import Category,Product,Customer,order

class Categorypro(admin.ModelAdmin):
    list_display = ['name']

class Productcate(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'image', 'description']

class customer(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'phone', 'email', 'password' ]

class Orderpro(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'price', 'phone', 'address', 'date']

# Register your models here.
admin.site.register(Category,Categorypro)
admin.site.register(Product,Productcate)
admin.site.register(Customer,customer)
admin.site.register(order,Orderpro)


