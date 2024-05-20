from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.urls.base import reverse_lazy
from portfolio.models import Unit
from django.views.generic import (View,ListView, DetailView, RedirectView)

# Crete home view

class ListingListView(ListView):
    paginate_by = 6
    model = Unit
    template_name = 'listings/available_unit_list.html'
    def get_queryset(self):
        return super().get_queryset().filter(is_occupied=False) 

class ListingDetailView(DetailView):
    model = Unit
    template_name = 'listings/listing_detail.html'

    success_url = reverse_lazy('listing-home')

class UnitLikeToggleRedirect(RedirectView):
    model = Unit

    def get_redirect_url(self, pk):
        obj = get_object_or_404(Unit, pk=pk)
        user = self.request.user
        print (obj.name + ' '+ user.email)

        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return reverse_lazy('listing-home') 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

class UnitLikeAPIToggle(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,pk, format=None):
        obj = get_object_or_404(Unit, pk=pk)
        user = self.request.user
        updated = False
        liked = False

        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
                liked = False
            else:
                obj.likes.add(user)
                updated = True
                liked = True

        data = {
            "updated": updated,
            "liked": liked
        }
        return Response(data) 
