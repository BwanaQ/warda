from django.urls import path
from api.v1.views import get_dashboard_data,load_neighbour_data


urlpatterns = [
    path('', get_dashboard_data, name='dashboard-data'),
    path('load-data', load_neighbour_data, name='load-neigh-data'),
    
]
