import pytest

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

from blog.models import Post, Category


@pytest.mark.django_db
def test_postmodel(start_setup):
    comment, post, cat = start_setup
    assert post.author.email == settings.DEFAULTUSERMAIL
    assert str(post) == post.title
    assert post.get_absolute_url() == "/pierwszy-post"
    assert post.img.url == post.img_url
    assert Post.published.count() == 2

    post.status = 0
    post.save()
    assert Post.published.count() == 1

    post.tags.add("apple, ball cat dog")
    tags = [str(x) for x in post.tags.all()]
    assert tags == ["apple, ball cat dog"]


@pytest.mark.django_db
def test_categorymodel(start_setup):
    comment, post, category = start_setup
    assert category.name == str(category)
    assert category.get_absolute_url() == "/category/python"
