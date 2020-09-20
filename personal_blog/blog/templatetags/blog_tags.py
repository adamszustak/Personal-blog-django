from django import template
from django.conf import settings

from blog.models import Post


register = template.Library()


@register.simple_tag
def blog_title():
    return settings.BLOG_TITLE


@register.simple_tag
def blog_description():
    return settings.BLOG_DESCRIPTION


@register.simple_tag
def blog_url():
    return settings.BLOG_URL


@register.simple_tag
def keywords_default():
    return settings.KEYWORDS


@register.simple_tag
def keywords(tags):
    return ", ".join(str(tag) for tag in tags)


@register.filter
def add_dash(string):
    if string:
        return "- " + string
    return string


@register.inclusion_tag("blog/snippets/latests_posts.html")
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by("-created_on")[:count]
    return {"latests_posts": latest_posts}
