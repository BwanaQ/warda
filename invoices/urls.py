from django.urls import path 
from .views import (
    InvoiceCreateView,
    InvoiceUpdateView,
    InvoiceDeleteView,
    InvoiceDetailView,
    InvoiceListView,
)

urlpatterns = [
    path('invoice/new', InvoiceCreateView.as_view(), name="create-invoice"),
    path('<int:pk>/invoice/update', InvoiceUpdateView.as_view(), name='update-invoice'),
    path('invoice/list', InvoiceListView.as_view(), name='invoice-list'),
    path('<int:id>/invoice/delete', InvoiceDeleteView.as_view(), name='delete-invoice'),
    path('<int:pk>/invoice/detail', InvoiceDetailView.as_view(), name='invoice-detail'),

]