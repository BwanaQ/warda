
from django.contrib import admin
from django.urls import path, include
from portfolio.views import (
    HomeView,
    AboutView,
    PropertyListView
)
from authentication.views import (
    ForgotPassword
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('contacts/', include('crm.urls')),
    path('invoices/', include('invoices.urls')),
    path('applications/', include('application_and_lease_management.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('property/manage/',include('property_inventory_and_conditions.urls')),
    path('locations/' , include('locations.urls')),
    path('service/management/', include('service_management.urls')),
    path('api/v1/', include('api.urls')),
    # path('application_and_lease_management/', include('application_and_lease_management.urls')),
    # Pages
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('properties/', PropertyListView.as_view(), name='properties'),
    path('forgot-password/', ForgotPassword.as_view(), name='forgot-password'),

    

]
