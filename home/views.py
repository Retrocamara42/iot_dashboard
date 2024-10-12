from django.shortcuts import render
from django.views.generic.base import TemplateView

# VIEWS
######################################################
"""
HomeView: Home view of underground cuy
"""
class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


"""
DeviceView: Devices' view of underground cuy
"""
class DeviceView(TemplateView):
    template_name = "home/devices.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context