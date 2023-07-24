from django import forms
from .models import Order



TYPE_CHOICES= (
    ('y', 'سالانه'),
    ('m', 'ماهانه'),
    ('d', 'روزانه'),
)

REPORT_CHOICES= (
    ('order', 'سفارش ها'),
    ('order_item', 'آیتم های سفارش ها'),
)

class OrderForm(forms.Form):
    addres=forms.CharField(label='آدرس',widget=forms.TextInput(attrs={'class':'form-control'}))
    code_post=forms.CharField(label='کدپستی',widget=forms.TextInput(attrs={'class':'form-control'}))


class CouponForm(forms.Form):
    code= forms.CharField(label='کد تخفیف')


class ReportDateForm(forms.Form):
    year = forms.IntegerField(label='سال',widget=forms.NumberInput(attrs={'class':'form-control'}))
    month = forms.IntegerField(label='ماه',widget=forms.NumberInput(attrs={'class':'form-control'}))
    day = forms.IntegerField(label='روز',widget=forms.NumberInput(attrs={'class':'form-control'}))
    report_type= forms.CharField(label='نوع گزارش', widget=forms.Select(choices=TYPE_CHOICES))
    report= forms.CharField(label='گزارش از', widget=forms.Select(choices=REPORT_CHOICES))
    # date = forms.DateField(widget=forms.DateInput(attrs={'id':'datepicker'}))
    # class Meta:
    #     model = Order
    #     fields =('updated',)
    #     widgets = {
    #     'updated': forms.DateInput(attrs={'id':'datepicker'},),
    #     }
    #     labels ={
    #         'created' : 'تاریخ'
    #     }

