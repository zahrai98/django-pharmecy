from django.urls import path,re_path
from . import views


app_name='orders'
urlpatterns = [
    path('create/',views.order_create,name='create'),
    path('<int:order_id>/',views.detail,name='detail'),
    path('payment/<int:order_id>/<price>',views.payment , name='payment'),
    path('verify/',views.verify , name='verify'),
    path('apply/<int:order_id>/',views.coupon_apply,name='coupon_apply'),
    path('order_detail/<int:order_id>/',views.order_detail,name='order_detail'),
    path('order_remove/<int:order_id>/',views.order_remove,name='order_remove'),
    # re_path(r'^report/(?P<type>(y|m|d)?)/<int:time>/$',views.report , name ='report'),
    re_path(r'^report/$',views.report , name ='report'),
]
