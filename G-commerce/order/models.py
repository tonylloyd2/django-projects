from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product
from user.models import generate_id


def coupon_uid():
    while True:
        uid = generate_id(15)
        checkuid = Coupon.objects.filter(coupon_id=uid)
        if not checkuid:
            break
    return uid

UserModel = get_user_model()

class Order(models.Model):
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return "{}->{}".format(self.user,self.product)

class Shipping(models.Model):
    shipping_type = models.CharField(max_length=20)
    shipping_fee = models.IntegerField()

    def __str__(self):
        return self.shipping_type

class PickupStation(models.Model):
    county = models.CharField(max_length=50)
    town = models.CharField(max_length=50)
    station = models.CharField(max_length=150)

    def __str__(self):
        return "{}->{}->{}".format(self.county,self.town,self.station)

class Coupon(models.Model):
    coupon_id = models.CharField(max_length=20,primary_key=True,default=coupon_uid)
    coupon_type = models.CharField(max_length=50,choices=(['shipping','shipping'],['discount','discount']))
    coupon_discount = models.IntegerField(default=0)
