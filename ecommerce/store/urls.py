from django.urls import path

from .views import *

app_name='store'

urlpatterns=[
      path('', homepage, name='homepage'),
      path('products/', products, name='products'),
      path('register/', register, name='register'),
      path('login/', login_request, name='login'),
      path('logout/', logout_request, name='logout'),
      path('user/', userpage, name='userpage'),
]