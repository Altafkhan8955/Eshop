from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=150, default='')
    image = models.ImageField(upload_to='upload/product/')


    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in =ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_all_products()
        

class Customer(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=250)



    @staticmethod
    def get_user_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False
        
class order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    phone = models.CharField(max_length=14)
    address = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

   


        
 

    

