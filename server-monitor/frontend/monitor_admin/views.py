from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
import requests
import json

from .models import Server, Notification
from .forms import ServerForm, NotificationForm


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class ServerListView(LoginRequiredMixin, ListView):
    model = Server
    template_name = 'admin/server_list.html'
    context_object_name = 'servers'
    paginate_by = 20

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Server.objects.all()
        return Server.objects.filter(owner=self.request.user)


class ServerCreateView(LoginRequiredMixin, CreateView):
    model = Server
    form_class = ServerForm
    template_name = 'admin/server_form.html'
    success_url = reverse_lazy('server-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Server created successfully!')
        return response


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # API call to get dashboard data
        try:
            response = requests.get('http://backend:8000/api/v1/monitoring/dashboard')
            context['dashboard_data'] = response.json() if response.status_code == 200 else {}
        except:
            context['dashboard_data'] = {}
        return context


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'admin/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Notification.objects.all()
        return Notification.objects.filter(user=self.request.user)