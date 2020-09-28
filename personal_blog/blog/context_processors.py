from blog.models import Category


def list_category(request):
    return {"category_list": Category.objects.all()}
