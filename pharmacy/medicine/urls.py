from django.urls import path,re_path
from . import views


app_name='medicine'
urlpatterns = [
    path('',views.home,name='home'),
    re_path(r'^category/(?P<slug>[\w-]+)/$',views.home,name='category_filter'),
    re_path(r'^brand/(?P<b_slug>[\w-]+)/$',views.home,name='brand_filter'),
    re_path(r'^(?P<slug>[\w-]+)/$',views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),
]
