from django.shortcuts import render,get_object_or_404,redirect
from .forms import CartAddForm
from .cart import Cart
from medicine.models import Product
from django.views.decorators.http import require_POST
from django.contrib import messages


def detail(request):
    cart = Cart(request)
    return render(request,'cart/detail.html',{'cart':cart})


@require_POST
def cart_add(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Product,id=product_id)
    form = CartAddForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        if product.count >= cd['quantity']:
            cart.add(product=product,quantity=cd['quantity'])
            messages.success(request,'با موفقیت به سبد خرید شما اضافه شد','success')
        else:
            messages.error(request,'موجودی کافی نیست','danger')
        return redirect('medicine:product_detail',product.slug)


def cart_remove(request,product_id):
    cart=Cart(request)
    product=get_object_or_404(Product,id=product_id)
    cart.remove(product)
    messages.success(request,'با موفقیت پاک شد','succuss')
    return redirect('cart:detail')


