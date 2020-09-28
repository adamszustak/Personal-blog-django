from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField
from conf.utils import get_default_user
from django_resized import ResizedImageField
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True, null=False)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:post_category", kwargs={"slug": self.slug})

    @property
    def published_post(self):
        return self.post_set.filter(status=1)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status=1)


class Post(models.Model):
    STATUS = ((0, "Draft"), (1, "Publish"))

    field = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, null=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, default=get_default_user
    )
    content = RichTextUploadingField()
    img = ResizedImageField(
        size=[1600, 1200], upload_to="post_pics", default="default.jpg"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    objects = models.Manager()
    tags = TaggableManager()
    published = PublishedManager()

    class Meta:
        ordering = ["status", "-created_on"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    @property
    def img_url(self):
        return self.img.url

    def recomended_posts(self):
        tags = self.tags.values_list("id", flat=True)
        posts = Post.published.filter(tags__in=tags).exclude(id=self.id)
        posts = posts.annotate(same_tags=Count("tags")).order_by(
            "-same_tags", "-created_on"
        )
        return posts
