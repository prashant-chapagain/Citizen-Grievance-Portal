from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
   
    
    # User grievance management
    path('grievances/submit/', views.submit_grievance, name='submit_grievance'),
    path('grievances/my/', views.my_grievances, name='my_grievances'),
    path('grievances/<str:reference_id>/', views.grievance_detail, name='grievance_detail'),
    
    # Change these admin routes to use 'staff/' prefix instead of 'admin/'
    path('staff/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff/grievances/', views.admin_grievance_list, name='admin_grievance_list'),
    path('staff/grievances/<str:reference_id>/', views.admin_grievance_detail, name='admin_grievance_detail'),
]