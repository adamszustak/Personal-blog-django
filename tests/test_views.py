from django.conf import settings
from django.contrib.auth.models import User
from django.urls import resolve, reverse

import pytest
from blog.models import Category, Post
from conf.utils import render_to_pdf
from terms_conditions.models import TermCondition


@pytest.mark.django_db
def test_view_postlist_GET(start_setup, client):
    url = reverse("blog:home")
    response = client.get(url)
    assert response.status_code == 200
    assert str(response.context["object_list"]) == "<Page 1 of 1>"
    assert "blog/home.html" in (t.name for t in response.templates)

    resolver = resolve("/")
    assert resolver.view_name == "blog:home"


@pytest.mark.django_db
def test_view_postdetail_GET(start_setup, client):
    post = Post.objects.get(slug="pierwszy-post")
    url = reverse("blog:post_detail", kwargs={"slug": post.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["form"] != None
    assert response.context["comments"] != None
    assert response.context["tags"] != None
    assert response.context["recomended_posts"] != None
    assert "blog/post_detail.html" in (t.name for t in response.templates)

    resolver = resolve("/pierwszy-post")
    assert resolver.view_name == "blog:post_detail"


@pytest.mark.django_db
def test_view_postdetail_POST(start_setup, client):
    post = Post.objects.get(slug="pierwszy-post")
    url = reverse("blog:post_detail", kwargs={"slug": post.slug})
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
    assert (
        str(messages[0])
        == "robot1 - twój post został wysłany do zatwierdzenia przez administratora"
    )
    assert response.status_code == 200
    assert post.comments.count() == 3
    assert "blog/post_detail.html" in (t.name for t in response.templates)


@pytest.mark.django_db
def test_view_postdetail_POST_nodata(start_setup, client):
    post = Post.objects.get(slug="pierwszy-post")
    url = reverse("blog:post_detail", kwargs={"slug": post.slug})
    response = client.post(url)
    assert response.context["form"] != None
    assert response.status_code == 200
    assert "blog/post_detail.html" in (t.name for t in response.templates)
    assert post.comments.count() == 2


@pytest.mark.django_db
def test_view_filterpost_GET(start_setup, client):
    qs = Post.objects.filter(title="Drugi post")
    url = reverse("blog:filter_post")
    response = client.get(url, {"q": "Drugi"})
    assert response.status_code == 200
    assert len(qs) == len(response.context["object_list"])
    assert "blog/home.html" in (t.name for t in response.templates)
    assert response.context["object_list"].count() == 1

    resolver = resolve("/szukaj/")
    assert resolver.view_name == "blog:filter_post"


@pytest.mark.django_db
def test_view_categorypost_GET(start_setup, client):
    url = reverse("blog:post_category", args=["python"])
    response = client.get(url)
    assert response.status_code == 200
    assert "blog/home.html" in (t.name for t in response.templates)
    assert response.context["object_list"].count() == 2

    resolver = resolve("/category/python")
    assert resolver.view_name == "blog:post_category"


@pytest.mark.django_db
def test_view_tagpost_GET(start_setup, client):
    post = Post.objects.get(slug="drugi-post")
    post.tags.add("it")
    qs = Post.objects.filter(tags__slug="it")
    response = client.get(reverse("blog:tag_post", args=["it"]))
    assert response.status_code == 200
    assert "blog/home.html" in (t.name for t in response.templates)
    assert response.context["object_list"].count() == 1

    resolver = resolve("/tag/it")
    assert resolver.view_name == "blog:tag_post"


@pytest.mark.django_db
def test_404(client):
    response = client.get("/404")
    assert response.status_code == 404
    assert "404.html" in (t.name for t in response.templates)
    assert "404" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_view_html(start_setup, client):
    post = Post.objects.get(slug="drugi-post")
    url = reverse("blog:generate_pdf", kwargs={"slug": post.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert "application/pdf" in response["content-type"]
    assert (
        f'inline; filename="{settings.BLOG_TITLE} - {post.title}.pdf"'
        in response["Content-Disposition"]
    )

    resolver = resolve("/generate/pdf/pierwszy-post")
    assert resolver.view_name == "blog:generate_pdf"


@pytest.mark.django_db
def test_sitemap(start_setup, client):
    response = client.get("/sitemap.xml")
    assert response.status_code == 200


@pytest.mark.django_db
def test_terms_conditions(start_setup, client):
    TermCondition.objects.create(text="not ok", newest=True)
    url = reverse("terms:terms_conditions")
    response = client.get(url)
    assert response.status_code == 200

    resolver = resolve("/law/terms-conditions/")
    assert resolver.view_name == "terms:terms_conditions"
