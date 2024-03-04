from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from.import views
from store import views
from .views import assign_terminal
from django.urls import path
from .views import approve_user, reject_user
from django.conf.urls import include
from store import routing
 

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
   path('reg.html',views.reg,name="reg"),
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
   #path('viewstaff/', views.viewstaff, name='viewstaff'),
   #path('accounts/login/', views.login, name='login'),
    path('logout/',views.logout,name="logout"),
    path('route',views.route,name="route"),
    path('route_view',views.route_view,name="route_view"),
    path('allocate_terminal_staff/', views.allocate_terminal_staff, name='allocate_terminal_staff'),
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
    path('term_staff_view/', views.term_staff_view, name='term_staff_view'), 
    path('bus_route_view/<int:bus_id>/', views.bus_route_view, name='bus_route_view'),
    path('assign_terminal/<int:terminal_id>/', assign_terminal, name='assign_terminal'),
    path('assign_terminal/', assign_terminal, name='assign_terminal'), 
    path('allocate_bus/', views.allocate_bus, name='allocate_bus'),
    path('staffrouteview/<int:bus_id>/', views.staffrouteview, name='staffrouteview'),
    path('daily_collection_sent/<int:user_id>/', views.daily_collection_sent, name='daily_collection_sent'),
    path('daily_collection_view/<int:user_id>/', views.daily_collection_view, name='daily_collection_view'),
    path('change_password/<int:terminal_id>/', views.change_password, name='change_password'),
    path('change_password/', views.change_password, name='change_password'),
    path('change_password/<int:terminal_id>/', views.change_password, name='change_password'),
    path('change_password/<int:terminal_id>/', views.change_password, name='change_password'),
    path('complaint/<int:user_id>/', views.complaint, name='complaint'),
    path('user_complaints/<int:user_id>/',views.user_complaints, name='user_complaints'),
    path('user_complaints/<int:user_id>/', views.user_complaints, name='user_complaints'),
    path('edit_route/<int:route_id>/', views.edit_route, name='edit_route'),
    path('delete_route/<int:route_id>/', views.delete_route, name='delete_route'),
    path('view_terminal_complaints/<int:terminal_id>/', views.view_terminal_complaints, name='view_terminal_complaints'),
    path('view_term_daily_collection/<int:terminal_id>/', views.view_term_daily_collection, name='view_term_daily_collection'),
    path('complaint_replay/<int:complaint_id>/', views.complaint_replay, name='complaint_replay'),
    path('approve_user/<int:user_id>/', approve_user, name='approve_user'),
    path('reject_user/<int:user_id>/', reject_user, name='reject_user'),
    path('workshopadd', views.workshopadd, name='workshopadd'),
    path('change_pass/<int:workshop_id>/', views.change_pass, name='change_pass'),
    path('workshop_complaint/<int:user_id>/', views.workshop_complaint, name='workshop_complaint'),
    path('view_workshop',views.view_workshop,name="view_workshop"),
    path('edit_workshop/<int:workshop_id>/', views.edit_workshop, name='edit_workshop'),
    path('delete_workshop/<int:workshop_id>/', views.delete_workshop, name='delete_workshop'),
    path('chat', views.chat, name='chat'),
    path('view_workshop_complaint/<int:workshop_id>/', views.view_workshop_complaint, name='view_workshop_complaint'),
     path('ws/', include(routing.websocket_urlpatterns)),
    path('view_complaints/<int:user_id>/', views.view_complaints, name='view_complaints'),
    path('edit-complaint/<int:complaint_id>/', views.edit_complaint, name='edit_complaint'),
    path('delete_complaint/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', views.logout_view, name='logout'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chatbot/response/', views.chatbot_response, name='chatbot_response'),
    path('gview/<int:complaint_id>/', views.gview, name='gview'),
    path('work_com_res/<int:complaint_id>/', views.work_com_res, name='work_com_res'),
    path('view_com_res/<int:complaint_id>/', views.view_com_res, name='view_com_res'),
    path('edit_response/<int:response_id>/', views.edit_response, name='edit_response'),

    


]
 

    
    
    # path('login/', login_view, name='login_'),

    
