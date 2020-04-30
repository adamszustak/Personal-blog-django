from blog.models import Post, Category


def list_all(request):
    return {"last5post": Post.published.order_by("created_on")[0:5]}


def list_category(request):
    return {"category_list": Category.objects.all()}
