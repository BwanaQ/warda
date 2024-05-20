from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('landlord/signup/', views.LandlordSignUp.as_view(), name='landlord-signup'),
    path('tenant/signup/', views.TenantSignUp.as_view(), name='tenant-signup'),
    path('service_pro/signup/', views.ServicePROSignUp.as_view(), name='service-pro-signup'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('login/', views.Login.as_view(), name='login'),
    
    path('pricing/', views.Pricing.as_view(), name='pricing')
    
]
