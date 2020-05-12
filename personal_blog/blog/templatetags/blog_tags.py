from django import template
from django.conf import settings


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
