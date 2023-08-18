from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import CommonRegisterForm

class CommonRegisterView(CreateView):
    model = User
    form_class = CommonRegisterForm
    success_url = '/newsportal'


