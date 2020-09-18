import pytest

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse

from blog.admin import PostAdmin
from blog.models import Post


@pytest.mark.django_db
def test_adminblog(start_setup, client, request):
    my_model_admin = PostAdmin(model=Post, admin_site=AdminSite())
    assert str(my_model_admin) == 'blog.PostAdmin'
    assert my_model_admin.get_fieldsets(request) == [(None, {'fields': ['field', 'title', 'slug', 'author', 'content', 'img', 'status', 'tags', 'show_url']})]

    admin = User.objects.create_superuser(username='bob', email='bob@test.com', password='test')
    url = reverse('admin:blog_post_change', args=['2'])
    response = client.get(url)
    assert response.status_code == 302

    client.login(username='bob', password='test')
    response2 = client.get(url)
    assert response2.status_code == 200
