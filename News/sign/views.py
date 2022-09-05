from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import BaseRegisterForm
from django.views.generic.edit import CreateView

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'