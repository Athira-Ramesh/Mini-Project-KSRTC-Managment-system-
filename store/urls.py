from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from.import views
from store import views
#urlpatterns = [
    #path('',views.index,name="home"),
    #path('index.html',views.index,name="home"),
    #path('login.html',views.login,name="login"),
    #path('registration.html',views.registration,name="registration"),
    #path('dashboard/',views.dashboard,name="dashboard"),
urlpatterns = [  
   path('',views.index,name="index"),
   path('index.html',views.index,name="home"),
   path('registration.html',views.registration,name="registration"),
   path('login.html',views.login,name="login"),
   path('index',views.index,name="index"),
   path('dashboard',views.dashboard,name="dashboard"),
   path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]