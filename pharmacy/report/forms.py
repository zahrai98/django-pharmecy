from django import forms


TYPE_CHOICES= (
    ('y', 'سالانه'),
    ('m', 'ماهانه'),
    ('d', 'روزانه'),
)
REPORT_CHOICES= (
    ('order', 'سفارش ها'),
    ('order_item', 'آیتم های سفارش ها'),
)

class ReportDateForm(forms.Form):
    year = forms.IntegerField(label='سال',widget=forms.NumberInput(attrs={'class':'form-control'}))
    month = forms.IntegerField(label='ماه',widget=forms.NumberInput(attrs={'class':'form-control'}))
    day = forms.IntegerField(label='روز',widget=forms.NumberInput(attrs={'class':'form-control'}))
    report_type= forms.CharField(label='نوع گزارش', widget=forms.Select(choices=TYPE_CHOICES))
    report= forms.CharField(label='گزارش از', widget=forms.Select(choices=REPORT_CHOICES))
