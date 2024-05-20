from django.urls import path
from .views import (
    UnitInventoryView
)


urlpatterns=[
    path('unit/<pk>/inventory/', UnitInventoryView.as_view(), name="unit-inventory" )
]