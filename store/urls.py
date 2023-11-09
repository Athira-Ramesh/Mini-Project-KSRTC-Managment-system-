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
   path('admindashboard',views.admindashboard,name="admindashboard"),
   path('terminal_add',views.terminal_add,name="terminal_add"),
   path('view_staffs',views.view_staffs,name="view_staffs"),
   path('dashboard1',views.dashboard1,name="dashboard1"),
   path('bus',views.bus,name="bus"),
   path('bus_view',views.bus_view,name="bus_view"),
   path('staff_term', views.staff_term, name='staff_term'),
   path('bus_view/', views.bus_view, name='bus_view'),
   path('viewstaff/', views.viewstaff, name='viewstaff'),
   #path('accounts/login/', views.login, name='login'),
    path('logout/',views.logout,name="logout"),
    path('route',views.route,name="route"),
    path('route_view',views.route_view,name="route_view"),
    path('profile/', views.myprofile, name='myprofile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    #path('logout/', views.logout, name='logout'),
    #path('accounts/login/', views.login, name='login'),

    path('edit_bus/<int:bus_id>/', views.edit_bus, name='edit_bus'),
    path('delete_bus/<int:bus_id>/', views.delete_bus, name='delete_bus'),
]