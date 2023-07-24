from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import MyUserManager



class User(AbstractBaseUser):
    email= models.EmailField(max_length=100,unique=True,verbose_name='ایمیل')
    full_name= models.CharField(max_length=100,verbose_name='نام کامل')
    is_admin= models.BooleanField(default=False,verbose_name='ادمین بودن')
    is_active = models.BooleanField(default=True,verbose_name='فعال بودن')
    phone_number=models.IntegerField(blank=True,null=True,default=0,verbose_name='شماره تلفن')
    objects=MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        verbose_name= 'کاربر'
        verbose_name_plural='کاربران'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
