from django.shortcuts import render
import jdatetime
from .items import Items
from django.contrib.auth.decorators import user_passes_test
from .forms import ReportDateForm
from django.contrib import messages
from orders.models import Order



def report_items(orders):
    total = 0
    items_class = Items()

    for order in orders:
        for item in order.items.all():
            items_class.add(item.product,item.quantity)
            total +=item.get_cost()
    return items_class,total


def email_admin(user):
    return user.is_admin


@user_passes_test(email_admin,login_url='medicine:home')
def report(request):
    form = ReportDateForm()
    orders = None
    if request.method == 'POST':
        form = ReportDateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                if cd['report_type'] == 'y' :
                    year1 = jdatetime.date(cd['year'],1,1)
                    year2 = jdatetime.date(cd['year']+1,1,1)
                    orders = Order.objects.filter(paid = True,updated__gte = year1,updated__lt = year2)
                elif cd['report_type'] == 'm':
                    year1 = jdatetime.date(cd['year'],cd['month'],1)
                    year2 = jdatetime.date(cd['year'],cd['month']+1,1)
                    orders = Order.objects.filter(paid = True,updated__gte = year1,updated__lt = year2)
                else:
                    orders = Order.objects.filter(paid = True,updated = jdatetime.date(cd['year'],cd['month'],cd['day']))
                messages.success(request,' با موفقیت گزارش گرفته شد','success')
            except:
                messages.error(request,'اطلاعات معتبر نیست','success')
            if cd['report'] == 'order_item':
                items,total = report_items(orders)
                return render(request,'report/report_detail.html',{'form':form,'items':items,'total':total})
        else:
            form = ReportDateForm()
            orders = None
            messages.error(request,'اطلاعات معتبر نیست','success')


    return render(request,'report/report_form.html',{'form':form,'orders':orders})

