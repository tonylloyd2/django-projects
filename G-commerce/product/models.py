from django.db import models
from user.models import generate_id
from django.contrib.auth import get_user_model

UserModel = get_user_model()

def product_uid():
    while True:
        uid = generate_id(12)
        checkuid = Product.objects.filter(product_id=uid)
        if not checkuid:
            break

    return uid

class Category(models.Model):
    category_name = models.CharField(max_length=50)
    category_description = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Categories"

rating_range = ((0,0),(0.5,0.5),(1,1),(1.5,1.5),(2,2),(2.5,2.5),(3,3),(3.5,3.5),(4,4),(4.5,4.5),(5,5))
class Product(models.Model):
    product_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_id = models.CharField(max_length=20,default=product_uid,primary_key=True)
    product_name = models.CharField(max_length=50)
    product_rating = models.FloatField(default=0,choices=rating_range)
    product_price = models.IntegerField()
    product_image = models.ImageField(upload_to="products/")
    product_info = models.TextField(blank=True,null=True)
    product_total = models.IntegerField(default=0)
    product_sold = models.IntegerField(default=0)
    product_available = models.IntegerField(default=0)

    def __str__(self):
        return "{}->{}".format(self.product_category,self.product_name)

class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return "{}".format(self.product)

class RatingReview(models.Model):
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    review = models.TextField(blank=True,null=True)
    rating = models.FloatField(default=0,choices=rating_range)