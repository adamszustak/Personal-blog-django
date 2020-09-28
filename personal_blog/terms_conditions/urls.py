from django.urls import path

from .views import terms_conditions

app_name = "terms"

urlpatterns = [
    path("terms-conditions/", terms_conditions, name="terms_conditions"),
]
