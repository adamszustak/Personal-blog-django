import pytest

from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings

from blog.models import Post, Category
from comments.models import Comment, ReplyComment


@pytest.mark.django_db
def test_comment(start_setup):
    comment, post, category = start_setup
    assert comment.text == "12345678910121416182022"
    assert comment.is_approved == False
    assert comment.post.title == post.title
    assert comment.post.field.name == category.name
    assert post.comments.count() == 2

    comment.is_approved = True
    assert comment.is_approved == True
    assert comment.__str__() == "12345678910121416182"


@pytest.mark.django_db
def test_reply_comment(start_setup):
    comment, post, cat = start_setup
    reply = ReplyComment.objects.create(comment=comment, text="you're right")
    assert reply.author.email == settings.DEFAULTUSERMAIL
    assert comment.replies.count() == 1
    assert reply.__str__() == "you're right"
