
from django.urls import path
from .views import (
    BuildingListView,
    BuildingCreateView,
    BuildingDetailView,
    BuildingUpdateView,
    BuildingDeleteView,
    
    UnitListView,
    UnitCreateView,
    UnitDetailView,
    UnitUpdateView,
    UnitDeleteView,


    
)

urlpatterns = [
    path('buildings/', BuildingListView.as_view(), name="building_list"),
    path('building/<int:pk>/', BuildingDetailView.as_view(), name="building-detail"),
    path('building/new/', BuildingCreateView.as_view(), name="building-create"),
    path('building/<int:pk>/update/', BuildingUpdateView.as_view(), name="building-update"),
    path('building/<int:pk>/delete/', BuildingDeleteView.as_view(), name="building-delete"),

    path('building/<int:building_pk>/units/', UnitListView.as_view(), name='unit-home'),
    path('building/<int:building_pk>/unit/<int:pk>/', UnitDetailView.as_view(), name='unit-detail'),
    path('building/<int:building_pk>/unit/new/', UnitCreateView.as_view(), name='unit-create'),
    path('building/<int:building_pk>/unit/<int:pk>/update/', UnitUpdateView.as_view(), name='unit-update'),
    path('building/<int:building_pk>/unit/<int:pk>/delete/', UnitDeleteView.as_view(), name='unit-delete'),



]