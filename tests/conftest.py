import pytest

from django.conf import settings

from comments.models import Comment, ReplyComment
from blog.models import Category, Post



@pytest.fixture
def start_setup(db, django_user_model):
    adm = django_user_model.objects.create_superuser(
        username="adm", password="password", email=settings.DEFAULTUSERMAIL
    )
    cat = Category.objects.create(name="Python", is_active=True, slug='python')
    post = Post.objects.create(
        field=cat,
        title="Pierwszy post",
        slug="pierwszy-post",
        content="To jest testowy post",
        status=1,
    )
    post2 = Post.objects.create(
        field=cat,
        title="Drugi post",
        slug="drugi-post",
        content="12345678910121416182022",
        status=1,
        tags="pytest, draft python"
    )
    Comment.objects.create(post=post, author="machine", text="ok")
    comm = Comment.objects.create(post=post, author="robot", text="12345678910121416182022")
    return comm, post, cat