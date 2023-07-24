from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name='accounts'
urlpatterns = [
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('register/',views.user_register,name='register'),
    path('profile/',views.profile,name='profile'),
    path('relation/',views.relation,name='relation'),
    path('orders/',views.orders,name='orders'),
    path('reset/',views.UserPassReset.as_view(),name='reset_pass'),
    path('reset/done',views.PasswordResetDone.as_view(),name='password_reset_done'),
    path('confirm/<uidb64>/<token>/',views.PasswordResetConfirm.as_view(),name='password_reset_confirm'),
    path('confirm/done/',views.PasswordResetComplete.as_view(),name='password_reset_complete'),
]
