
from django.urls import path
from .views import (
    HomeView,
    ListingListView,
    ListingDetailView,
    UnitLikeToggleRedirect,
    UnitLikeAPIToggle
)

urlpatterns = [
    path('listing/list', ListingListView.as_view(), name="listing-list"),
    path('<int:pk>/', ListingDetailView.as_view(), name="listing-detail"),

    path('<int:pk>/like/', UnitLikeToggleRedirect.as_view(), name="unit-like-toggle"),
    path('api/<int:pk>/like/', UnitLikeAPIToggle.as_view(), name="api-unit-like-toggle"),
    
]    
