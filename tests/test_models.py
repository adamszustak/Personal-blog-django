import pytest

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

from blog.models import Post, Category
from comments.models import ReplyComment, Comment
from terms_conditions.models import TermCondition

@pytest.mark.django_db
def test_postmodel(start_setup):
    comment, post, post2, cat = start_setup
    assert post.author.email == settings.DEFAULTUSERMAIL
    assert str(post) == post.title
    assert post.get_absolute_url() == "/pierwszy-post"
    assert post.img.url == post.img_url
    assert Post.published.count() == 2

    post3 = Post.objects.create(
        field=cat,
        title="Trzeci post",
        slug="trzeci-post",
        content="12345678910121416182022",
        status=1,
    )
    post.tags.add('Django','Python')
    post3.tags.add('Django')
    assert list(post.recomended_posts()) == [post3]

    post2.tags.add('Django', 'Python', 'SQL')
    assert list(post.recomended_posts()) == [post2, post3]

    post.status = 0
    post.save()
    assert Post.published.count() == 2



@pytest.mark.django_db
def test_categorymodel(start_setup):
    comment, post, post2, category = start_setup
    assert category.name == str(category)
    assert category.get_absolute_url() == "/category/python" 


@pytest.mark.django_db
def test_comment(start_setup):
    comment, post, post2, category = start_setup
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
    comment, post, post2, category = start_setup
    reply = ReplyComment.objects.create(comment=comment, text="you're right")
    assert reply.author.email == settings.DEFAULTUSERMAIL
    assert comment.replies.count() == 1
    assert reply.__str__() == "you're right"



@pytest.mark.django_db
def test_termcondition():
    term1 = TermCondition.objects.create(
        text='not ok',
        newest=True
    )
    term2 = TermCondition.objects.create(
        text='ok', 
        newest=False
    )
    assert term1.newest == True

    term2.newest = True
    term2.save()
    assert TermCondition.objects.get(text='not ok').newest == False
    assert term2.newest == True