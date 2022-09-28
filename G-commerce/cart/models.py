from django.db import models
from django.contrib.auth import get_user_model
from order.models import Coupon, Shipping
from product.models import Product
UserModel = get_user_model()

def get_default_shipping():
    return Shipping.objects.get(shipping_type='standard')

class Cart(models.Model):
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    no_items = models.IntegerField(choices=([1,1],[2,2],[3,3]),default=1)
    shipping = models.ForeignKey(Shipping,on_delete=models.SET_NULL,null=True,default=get_default_shipping)
    coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return "{}->{}".format(self.user,self.product)

class WishList(models.Model):
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    no_items = models.IntegerField(choices=([1,1],[2,2],[3,3]),default=1)