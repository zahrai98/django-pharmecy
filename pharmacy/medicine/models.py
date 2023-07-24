from django.db import models
from django.urls import reverse
from django_jalali.db import models as jmodels
from django.conf import settings



class Brand(models.Model):
    name = models.CharField(max_length=200,verbose_name='نام برند')
    slug = models.SlugField(max_length=200 , unique=True ,verbose_name='اسلاگ',allow_unicode=True,)

    class Meta:
        ordering =('name',)
        verbose_name= 'برند'
        verbose_name_plural='برند ها'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('medicine:brand_filter',args=(self.slug,))


class Category(models.Model):
    name = models.CharField(max_length=200,verbose_name='نام دسته بندی')
    slug = models.SlugField(max_length=200 , unique=True,verbose_name='اسلاگ',allow_unicode=True)
    sub_category = models.ForeignKey('self',related_name='scategory',on_delete=models.CASCADE,blank=True,null=True,verbose_name='زیر دسته بندی')
    is_sub=models.BooleanField(default=False,verbose_name='زیر دسته بندی بودن')

    class Meta:
        ordering =('name',)
        verbose_name= 'دسته بندی'
        verbose_name_plural='دسته بندی ها'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('medicine:category_filter',args=(self.slug,))


class Product(models.Model):
    category= models.ManyToManyField(Category,related_name='products',verbose_name='دسته بندی')
    name = models.CharField(max_length=200,verbose_name='نام محصول')
    slug = models.SlugField(max_length=200 ,unique=True,verbose_name='اسلاگ',allow_unicode=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/',verbose_name='تصویر')
    description = models.TextField(verbose_name='توضیحات')
    price = models.PositiveBigIntegerField(verbose_name='قیمت')
    available = models.BooleanField(default=True,verbose_name='موجود بودن')
    count = models.PositiveBigIntegerField(verbose_name='تاریخ تعداد موجود')
    date_of_manufacture = jmodels.jDateField(verbose_name='تاریخ تولید')
    expiration_date = jmodels.jDateField(verbose_name='تاریخ انقضا')
    created= jmodels.jDateTimeField(auto_now_add=True,verbose_name='تاریخ ایجاد')
    updated = jmodels.jDateTimeField(auto_now=True,verbose_name='تاریخ اپدیت')
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,related_name='b_product',verbose_name='برند',blank=True,null=True)

    class Meta:
        ordering = ('name',)
        verbose_name= 'محصول'
        verbose_name_plural='محصولات'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('medicine:product_detail',args=(self.slug,))


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='ucomment')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='pcomment')
    reply = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='rcomment')
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=500)
    created = jmodels.jDateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}-{self.body[:30]}'

    class Meta:
        ordering = ('-created',)
        verbose_name= 'نظر'
        verbose_name_plural='نظرات'
