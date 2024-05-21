from django.urls import path
from .views import (
    home_view,
    AmenityCreateView,
    AmenityUpdateView,
    AmenityDeleteView,
    AmenityDetailView,
    AmenityListView,
    CommunityCreateView,
    CommunityUpdateView,
    CommunityDeleteView,
    CommunityDetailView,
    CommunityListView,
    OnboardingView,
    AddLeaseTemplateView,
    ServiceCategoryCreateView
)


from application_and_lease_management.forms import (
    LeaseTypeForm

)
from  locations.forms import (
    AddressForm

)

from .views import FORMS

from authentication.views import (
    UserListView,
    AgentListView,
    LandlordListView,
    TenantListView
)

from service_management.views import (
    ServiceRequestListView,
    ServiceCategoryListView,
    ServicePROJobsListView,
    ServiceRequestDetailView,
    CreateProposalView,
    ServicePROProposalListView
)

from messager.views import (
    InboxView
)

from portfolio.views import (
    BuildingListView,
    BuildingCreateView,
    BuildingUpdateView,
    BuildingDetailView,
    BuildingDeleteView,
    UnitListView,
    UnitCreateView,
    UnitDetailView,
    UnitUpdateView,
    UnitDeleteView,
)
urlpatterns = [
    path('', home_view, name='dashboard-home'),
    path('amenity/new', AmenityCreateView.as_view(), name='create-amenity'),
    path('<int:pk>/amenity/update', AmenityUpdateView.as_view(), name='update-amenity'),
    path('amenity/list', AmenityListView.as_view(), name='amenity-list'),
    path('<int:id>/amenity/delete', AmenityDeleteView.as_view(), name='delete-amenity'),
    path('<int:pk>/amenity/detail', AmenityDetailView.as_view(), name='amenity-detail'),

    path('building/new', BuildingCreateView.as_view(), name='create-building'),
    path('<int:pk>/building/update', BuildingUpdateView.as_view(), name='update-building'),
    path('building/list', BuildingListView.as_view(), name='building-list'),
    path('<int:id>/building/delete', BuildingDeleteView.as_view(), name='delete-building'),
    path('<int:pk>/building/detail', BuildingDetailView.as_view(), name='building-detail'),

    path('onboarding/landlord', OnboardingView.as_view(), name='onboarding'),
    path('community/new', CommunityCreateView.as_view(), name='create-community'),
    path('<int:pk>/community/update', CommunityUpdateView.as_view(), name='update-community'),
    path('community/list', CommunityListView.as_view(), name='community-list'),
    path('<int:id>/community/delete', CommunityDeleteView.as_view(), name='delete-community'),
    path('<int:pk>/community/detail', CommunityDetailView.as_view(), name='community-detail'),
    path('lease-template/new', AddLeaseTemplateView.as_view(FORMS,), name='create-lease-template'),
    path('users/', UserListView.as_view(), name= 'user-list'),
    path('agents/', AgentListView.as_view(), name='agent-list'),
    path('landlords/', LandlordListView.as_view(), name='landlord-list'),
    path('tenants/', TenantListView.as_view(), name='tenant-list'),
    path('service/requests', ServiceRequestListView.as_view(), name='service-requests'),
    path('service/categories', ServiceCategoryListView.as_view(), name='service-categories'),
    path('service_category/new', ServiceCategoryCreateView.as_view(), name='create-service-category'),
    path('service_pro/jobs', ServicePROJobsListView.as_view(), name='service-pro-jobs'),
    path('<int:pk>/job/detail', ServiceRequestDetailView.as_view(), name='service-pro-job-detail'),
    path('<int:pk>/create/proposal', CreateProposalView.as_view(), name='create-proposal'),
    path('service_pro/proposals',  ServicePROProposalListView.as_view(), name='service-pro-proposals'),
    path('inbox', InboxView.as_view(), name='inbox'),


]