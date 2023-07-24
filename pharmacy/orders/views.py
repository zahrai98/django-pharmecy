from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Order,OrderItem,Coupon
from cart.cart import Cart
from .forms import OrderForm,CouponForm,ReportDateForm
from django.contrib import messages
from django.http import HttpResponse
from suds.client import Client
from django.views.decorators.http import require_POST
from django.utils import timezone
from medicine.models import Product
import jdatetime
from .items import Items



@login_required
def detail(request,order_id):
    form = CouponForm()
    order=get_object_or_404(Order,id = order_id)
    for item in order.items.all():
        if item.product.count < item.quantity:
            messages.error(request,item.product.name +' موجودی کافی ندارد','danger')
            return redirect('cart:detail')
    return render(request,'orders/order.html',{'order':order,'form':form})


@login_required
def order_create(request):
    cart = Cart(request)
    for item in cart:
        if item['product'].count < item['quantity']:
            messages.error(request,item['product'].name +' موجودی کافی ندارد','danger')
            return redirect('cart:detail')
    if request.method == 'POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            order= Order.objects.create(user=request.user,addres=cd['addres'],code_post=cd['code_post'])
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
            cart.clear()
            messages.success(request,'sefaresh sabt shod','success')
            return redirect('orders:detail',order.id)
        else:
            messages.error(request,'info kamel nis','danger')
    else:
        form=OrderForm()
        return render(request,'orders/order_form.html',{'form':form})


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
mobile = '09123456789'  # Optional
CallbackURL = 'http://localhost:8000/orders/verify/' # Important: need to edit for realy server.


@login_required
def payment(request,order_id,price):
    global amount,o_id  # Toman / Required
    amount=price
    o_id=order_id
    result = client.service.PaymentRequest(MERCHANT, amount, description, request.user.email, mobile, CallbackURL)
    if result.Status == 100:
        try:
            order = get_object_or_404(Order,id = order_id)
            for item in order.items.all():
                product = Product.objects.get(id=item.product.id)
                product.count -= item.quantity
                if product.count == 0:
                    product.available=False
                product.save()
        except:
            messages.error(request,'مشکلی به وجود امده دوباره تلاش کنید','danger')
            return redirect('medicine:home')
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))


def count():
    order=Order.objects.get(id=o_id)
    try:
        for item in order.items.all():
            product = Product.objects.get(id=item.product.id)
            product.count += item.quantity
            if product.count > 0:
                product.available=True
            product.save()
    except:
        pass


@login_required
def verify(request):
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        order=Order.objects.get(id=o_id)
        if result.Status == 100:
            order.paid=True
            order.status = 'paid'
            order.save()
            messages.success(request,'Transaction was successful','success')
            return redirect('medicine:home')
            # return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            count()
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            count()
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        count()
        return HttpResponse('Transaction failed or canceled by user')

def coupon_apply(request,order_id):
    now=timezone.now()
    form =CouponForm(request.POST)
    if form.is_valid():
        code=form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__exact=code,valid_from__lte=now,valid_to__gte=now,active=True)
        except :
            messages.error(request,'this coupon does not exist','danger')
            return redirect('orders:detail',order_id)
        order =Order.objects.get(id=order_id)
        order.discount = coupon.discount
        order.save()
    return redirect('orders:detail',order_id)

def order_detail(request,order_id):
    order = Order.objects.get(id =order_id)
    return render(request,'orders/order_detail.html',{'order':order})

def order_remove(request,order_id):
    order = Order.objects.get(id =order_id)
    order.delete()
    messages.success(request,'سفارش با موفقیت حذف شد','success')
    return redirect('accounts:orders')


def report_items(orders):
    total = 0
    items_class = Items()

    for order in orders:
        for item in order.items.all():
            items_class.add(item.product,item.quantity)
            total +=item.get_cost()
    return items_class,total


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
                return render(request,'orders/report_detail.html',{'form':form,'items':items,'total':total})
        else:
            form = ReportDateForm()
            orders = None
            messages.error(request,'اطلاعات معتبر نیست','success')


    return render(request,'orders/report_form.html',{'form':form,'orders':orders})


#
# def report_items(orders):
#     items ={}
#     total = 0
#     for order in orders:
#         for item in order.items.all():
#             if item.product.id not in items.keys():
#                 items[item.product.id] = {'product':item.product.name ,'price': item.price,'quantity':item.quantity,'cost':item.get_cost()}
#                 total +=item.get_cost()
#             else:
#                 items[item.product.id]['quantity'] += item.quantity
#                 items[item.product.id]['cost'] += item.get_cost()
#                 total +=item.get_cost()
#     return items,total
