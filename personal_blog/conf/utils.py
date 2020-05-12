from xhtml2pdf import pisa

from io import BytesIO
from xhtml2pdf import pisa

from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.conf import settings


def get_default_user():
    return User.objects.get(email=settings.DEFAULTUSERMAIL)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(
        BytesIO(html.encode("UTF8")), result, encoding="UTF-8"
    )
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None
