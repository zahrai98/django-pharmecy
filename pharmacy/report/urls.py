from django.urls import path
from . import views


app_name='report'
urlpatterns = [
    path('report/',views.report , name ='report'),
]
