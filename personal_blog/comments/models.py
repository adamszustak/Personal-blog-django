from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.utils import timezone

from blog import models as blog_models
from conf.utils import get_default_user


class BaseComment(models.Model):
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def __str__(self):
        return self.text[0:20]


class Comment(BaseComment):
    post = models.ForeignKey(
        blog_models.Post, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.CharField(max_length=10)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_date"]

    def approve(self):
        self.is_approved = True
        self.save()

    def save(self, *args, **kwargs):
        old = self.__class__.objects.filter(
            id=getattr(self, str(id), None)
        ).first()
        if old:
            if old.is_approved != self.is_approved:
                cache.delete("comments")
        super(Comment, self).save(*args, **kwargs)


class ReplyComment(BaseComment):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="replies"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, default=get_default_user
    )
