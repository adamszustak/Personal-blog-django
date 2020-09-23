from django.core.exceptions import ValidationError
from django import forms
from django.contrib import admin, messages
from django.views.generic.edit import FormView, CreateView, UpdateView

from .models import TermCondition

admin.site.register(TermCondition)
