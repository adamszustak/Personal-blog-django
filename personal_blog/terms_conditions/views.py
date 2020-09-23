from django.shortcuts import render

from .models import TermCondition


def terms_conditions(request):
    terms = TermCondition.objects.filter(newest=True)[0] or None
    return render(request, "blog/generic_info.html", {"terms": terms.text})
