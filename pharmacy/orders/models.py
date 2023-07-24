from django.db import models
from django.conf import settings
from medicine.models import Product
from django.core.validators import MinValueValidator,MaxValueValidator
from django_jalali.db import models as jmodels


class Order(models.Model):

    STATUS_CHOICES = (
        ('registered','ثبت سفارش' ),
        ('paid','ثبت و پرداخت شده' ),
        ('sended','ارسال شد'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='orders',verbose_name='کاربر')
    created= jmodels.jDateField(auto_now_add=True,verbose_name='تاریخ ایجاد')
    updated = jmodels.jDateField(auto_now=True,verbose_name='تاریخ آپدیت ')
    paid = models.BooleanField(default=False,verbose_name='پرداخت شده')
    addres = models.TextField(verbose_name='آدرس')
    code_post = models.CharField(max_length=20,verbose_name='کد پستی')
    discount = models.IntegerField(blank=True,null=True,default=0,verbose_name='درصد تخفیف')
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='registered',verbose_name='وضعیت سفارش')

    class Meta:
        ordering = ('-created',)
        verbose_name= 'سفارش'
        verbose_name_plural='سفارش ها'

    def __str__(self):
        return f'{self.user} - {self.id}'

    @property
    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = (self.discount /100) * total
            return int(total - discount_price)
        return total
    

class OrderItem(models.Model):
    order= models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items',verbose_name='سفارش')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='order_items',verbose_name='محصول')
    price = models.IntegerField(verbose_name='قیمت')
    quantity=models.PositiveIntegerField(default=1,verbose_name='تعداد')

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity


class Coupon(models.Model):
    code = models.CharField(max_length=30,unique=True,verbose_name='کد تخفیف')
    valid_from = jmodels.jDateField(verbose_name='تاریخ اعتبار از')
    valid_to = jmodels.jDateField(verbose_name='تاریخ اعتبار تا')
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)],verbose_name='درصد تخفیف')
    active = models.BooleanField(default=False,verbose_name='فعال بودن')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name= 'تخفیف'
        verbose_name_plural='تخفیف ها'
