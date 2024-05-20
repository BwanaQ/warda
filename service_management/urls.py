from django.urls import path
from service_management.views import *

urlpatterns = [
path('building/<int:building_pk>/unit/<int:unit_pk>/', UnitMaintainanceRequestView.as_view(), name='service_requests-request'),
]