from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import TemplateView, ListView
from .models import Customers
from django.http import HttpResponseRedirect
from .forms import CustNumberForm


def logout(request):
    auth.logout(request)
    return redirect('/')

class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'customersearch.html'

class SearchResultsView(LoginRequiredMixin, ListView):
    model = Customers
    template_name = 'customersearchresults.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Customers.objects.filter(
            Q(name__icontains=query) | Q(customer_account__icontains=query)
        )
        return object_list 
