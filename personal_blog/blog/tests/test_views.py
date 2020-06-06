import pytest

from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

from blog.models import Post, Category


@pytest.mark.django_db
def test_view_postlist_GET(start_setup, client):
    url = reverse("home")
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == 2 
    assert 'blog/home.html' in (t.name for t in response.templates)


@pytest.mark.django_db
def test_view_postdetail_GET(start_setup, client):
    post = Post.objects.get(slug="pierwszy-post")
    url = reverse("post_detail", kwargs={"slug" : post.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["form"] != None
    assert response.context["comments"] != None
    assert response.context["tags"] != None
    assert 'blog/post_detail.html' in (t.name for t in response.templates)


@pytest.mark.django_db
def test_view_postdetail_POST(start_setup, client):
    post = Post.objects.get(slug="pierwszy-post")
    url = reverse("post_detail", kwargs={"slug" : post.slug})
    response = client.post(
        url,
        {
            "post": Post.objects.get(title="Pierwszy post"),
            "author": "robot1",
            "text": "ok",
        },
    )
    messages = list(response.context["messages"])
    assert len(messages) == 1
    assert str(messages[0]) == "robot1 - twój post został wysłany do zatwierdzenia przez administratora"
    assert response.status_code ==  200
    assert post.comments.first().author == "robot1"
    assert post.comments.count() == 3
    assert 'blog/post_detail.html' in (t.name for t in response.templates)

@pytest.mark.django_db
def test_view_postdetail_POST_nodata(start_setup, client):
    post = Post.objects.get(slug="pierwszy-post")
    url = reverse("post_detail", kwargs={"slug" : post.slug})
    response = client.post(url)
    assert response.context["form"] != None
    assert response.status_code ==  200
    assert 'blog/post_detail.html' in (t.name for t in response.templates)
    assert post.comments.count() == 2

@pytest.mark.django_db
def test_view_filterpost_GET(start_setup, client):
    qs = Post.objects.filter(title="Drugi post")
    url = reverse("filter_post")
    response = client.get(url, {"q": "Drugi"})
    assert response.status_code ==  200
    assert len(qs) == len(response.context["object_list"])
    assert 'blog/home.html' in (t.name for t in response.templates)
    assert response.context["object_list"].count() ==  1

@pytest.mark.django_db
def test_view_categorypost_GET(start_setup, client):
    url = reverse("post_category", args=["python"])
    response = client.get(url)
    assert response.status_code ==  200
    assert 'blog/home.html' in (t.name for t in response.templates)
    assert response.context["object_list"].count() == 2

@pytest.mark.django_db
def test_view_tagpost_view_GET(start_setup, client):
    post = Post.objects.get(slug="drugi-post")
    post.tags.add("it")
    qs = Post.objects.filter(tags__slug="it")
    response = client.get(reverse("tag_post", args=["it"]))
    assert response.status_code ==  200
    assert 'blog/home.html' in (t.name for t in response.templates)
    assert response.context["object_list"].count() == 1

@pytest.mark.django_db
def test_404(client):
    response = client.get("/404")
    assert response.status_code == 404
    assert 'blog/404.html' in (t.name for t in response.templates)
    assert "404" in response.content.decode("utf-8")
from conf.utils import render_to_pdf
@pytest.mark.django_db
def test_view_html(start_setup, client):
    post = Post.objects.get(slug="drugi-post")
    url = reverse("generate_pdf", kwargs={"slug" : post.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert "application/pdf" in response['content-type']
    assert f'inline; filename="{settings.BLOG_TITLE} - {post.title}.pdf"' in response["Content-Disposition"]