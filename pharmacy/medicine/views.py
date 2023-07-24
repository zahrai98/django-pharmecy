from django.shortcuts import render,get_object_or_404
from .models import Category,Product,Brand,Comment
from cart.forms import CartAddForm
from django.core.paginator import Paginator
from .forms import AddCommentForm
from django.contrib import messages


def home(request,slug=None,b_slug=None):
    categories=Category.objects.filter(is_sub=False)
    products=Product.objects.filter(available=True)
    brands = Brand.objects.all()
    if slug:
        category=get_object_or_404(Category,slug=slug)
        products=products.filter(category=category)
    elif b_slug:
        brand=get_object_or_404(Brand,slug=b_slug)
        products=products.filter(brand=brand)

    paginator = Paginator(products,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'medicine/home.html',{'categories':categories,'brands':brands ,'page_obj':page_obj})


def product_detail(request,slug):
    product=get_object_or_404(Product,slug=slug)
    if request.method == 'POST':
        comment_form = AddCommentForm(request.POST)
        if comment_form.is_valid():
            new_comment =comment_form.save(commit=False)
            new_comment.product = product
            new_comment.user = request.user
            new_comment.save()
            messages.success(request,'نظر شما با موفقیت ثبت شد','succuss')
    else:
            comment_form= AddCommentForm()
    form =CartAddForm()
    comments = Comment.objects.filter(product=product,is_reply=False)
    paginator = Paginator(comments,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'medicine/product_detail.html',
                  {'product':product,'page_obj':page_obj,'form':form,'comment_form':comment_form})


def search(request):
    data= request.GET.get('search')

    products = Product.objects.filter(name__icontains=data)
    categories = Category.objects.filter(is_sub=False)
    brands = Brand.objects.all()

    paginator = Paginator(products,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'medicine/home.html',{'categories':categories,'brands':brands ,'page_obj':page_obj})

