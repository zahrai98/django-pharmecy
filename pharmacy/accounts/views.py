from django.shortcuts import render,redirect,get_object_or_404
from .forms import UserLoginForm,UserRegisterForm,UserEditForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import User
from orders.models import Order
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


def user_login(request):
    if request.method == 'POST':
        form=UserLoginForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request,email=cd['email'], password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'you logged in succesfully','success')
                return redirect('medicine:home')
            else:
                messages.error(request,'username or pass is wrong','danger')
    else:
        form=UserLoginForm()
    return render(request,'accounts/login.html',{'form':form})


def user_logout(request):
    logout(request)
    messages.success(request,'you logged out succesfully','success')
    return redirect('medicine:home')


def user_register(request):
    if request.method == 'POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=User.objects.create_user(cd['email'],cd['full_name'],cd['password'])
            user.save()
            messages.success(request,'you registerd succesfully','success')
            return redirect('accounts:login')
    else:
        form=UserRegisterForm()
    return render(request,'accounts/register.html',{'form':form})



def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST , instance=user)
        if form.is_valid():
            user = form.save()
            messages.success(request,'اطلاعات با موفقیت ویرایش شد','success')
            return redirect('accounts:profile')
    form = UserEditForm(instance=user)
    return render(request,'accounts/profile.html',{'form':form ,'user':user})


def relation(request):
    return render(request,'accounts/relation.html')


def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request,'orders/orders_list.html',{'orders':orders})


class UserPassReset(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'

class PasswordResetDone(auth_views.PasswordResetDoneView):
    template_name = 'accounts/reset_done.html'

class PasswordResetConfirm(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class PasswordResetComplete(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
