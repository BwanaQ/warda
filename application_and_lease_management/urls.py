from django.urls import path 
from .views import (
    ApplicationCreateView,
    ApplicationUpdateView,
    ApplicationDeleteView,
    ApplicationDetailView,
    ApplicationListView,
    ApproveApplicationView
)

urlpatterns = [
    path('application/new', ApplicationCreateView.as_view(), name="create-application"),
    path('<int:pk>/application/update', ApplicationUpdateView.as_view(), name='update-application'),
    path('application/list', ApplicationListView.as_view(), name='application-list'),
    path('<int:id>/application/delete', ApplicationDeleteView.as_view(), name='delete-application'),
    path('<int:pk>/application/detail', ApplicationDetailView.as_view(), name='application-detail'),
    path('approve', ApproveApplicationView.as_view(), name='approve-application')

]