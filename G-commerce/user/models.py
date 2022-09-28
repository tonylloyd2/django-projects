from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
import random

def generate_id(length):
    return ''.join(
        random.SystemRandom().choice([chr(i) 
        for i in range(97, 123)] + [str(i) for i in range(length)]) 
        for _ in range(length)
    )


class UserManager(BaseUserManager):
    def create_superuser(self,email, password):

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
def user_uid():
    while True:
        uid = generate_id(12)
        checkuid = User.objects.filter(user_id=uid)
        if not checkuid:
            break
    return uid

class User(AbstractBaseUser,PermissionsMixin):
    user_id = models.CharField(max_length=20,blank=False,null=False,primary_key=True,default=user_uid)
    email = models.EmailField(max_length=150,null=False,blank=False,unique=True)
    first_name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    phone_number = models.CharField(max_length=20,null=True,blank=True)
    pickup_station = models.TextField(null=True,blank=True,default="You have not specified a pickup station")
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

