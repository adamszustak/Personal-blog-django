from blog.models import Post, Category


def list_category(request):
    return {"category_list": Category.objects.all()}
