from django.urls import path,include
from .views import signup,loginview,question,answer,top,home,result,logoutview,logout_success,signup_success


urlpatterns=[
    path('top/',top,name='top'),
    path('signup/',signup,name='signup'),
    path('signup_success/',signup_success,name="signup_success"),
    path('loginview/',loginview,name='loginview'),
    path('home/',home,name='home'),
    path('question/',question,name='question'),
    path('answer/<int:ans>',answer,name="answer"),
    path('result/',result,name="result"),
    path('logoutview/',logoutview,name="logoutview"),
    path('logout_success/',logout_success,name="logout_success"),
    path('accounts/',include('django.contrib.auth.urls')),
]