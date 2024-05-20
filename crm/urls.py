from django.urls import path 
from .views import (
    ContactView,
    ContactCreateView,
    ContactUpdateView,
    ContactDeleteView,
    ContactDetailView,
    ContactListView,
)

urlpatterns = [
    path('', ContactView.as_view(), name="contact"),
    path('contact/new', ContactCreateView.as_view(), name="create-contact"),
    path('<int:pk>/contact/update', ContactUpdateView.as_view(), name='update-contact'),
    path('contact/list', ContactListView.as_view(), name='contact-list'),
    path('<int:id>/contact/delete', ContactDeleteView.as_view(), name='delete-contact'),
    path('<int:pk>/contact/detail', ContactDetailView.as_view(), name='contact-detail'),

]