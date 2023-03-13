from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf import Settings
from django.conf.urls.static import static
from .models import*
from django.contrib.auth.hashers import make_password,check_password
from django.views import View
from store.models import Product
from store.models import Customer
from store.models import order


# Create your views here.

class index(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        return redirect('index')



    def get(self,request):
        cart = request.session.get('cart')
        if not cart:
            request.session.cart = {}
        products = None
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products()
            data={
                 'product' : products,
                 'category' : categories
                }
            return render(request,"index.html",data)

class signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        firstname = postData.get('firstname')
        lastname = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        cpassword = postData.get('cpassword')    
        # validation
        value = {
            'firstname': firstname,
            'lastname': lastname,
            'phone': phone,
            'email': email
        }
        error_message = None
        if password == cpassword:
            user = Customer(firstname=firstname,
                            lastname=lastname,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = self.validateuser(user)

        if not error_message:
            user.password = make_password(user.password)
            user.save()
            return redirect('index')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validateuser(self, user):
        if (not user.firstname):
            error_message = "First Name Required !!"
        elif len(user.firstname) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not user.lastname:
            error_message = 'Last Name Required'
        elif len(user.lastname) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not user.phone:
            error_message = 'Phone Number required'
        elif len(user.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(user.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(user.email) < 5:
            error_message = 'Email must be 5 char long'
        elif Customer.objects.filter(email=user.email):
            error_message = "Email already exist"
        #elif user.isExists():
           # error_message = 'Email Address Already Registered..'
        # saving

        return error_message
    
class login(View):
    def get(self, request):
        return render(request,"login.html")

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = Customer.get_user_by_email(email)
        error_message = None
        if user:
            flag = check_password(password, user.password)
            if flag:
                request.session['id'] = user.id
                return redirect('index')
            else:
                error_message = "Email or password invalid"
        else:
            error_message = "Email or password invalid"
        return render(request,"login.html",{'error':error_message})

def logout(request):
    request.session.clear()
    return redirect('login')

class cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        return render(request,'cart.html',{'products':products})
    
class checkout(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))

        for product in products:
            Orders = order(
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            Orders.save()
        request.session['cart'] = {}

        return redirect('cart')
    
class Orderview(View):
    def get(self, request):    
            orders = order.objects.all().order_by('-date')
            return render(request,"orders.html",{'orders':orders})
    