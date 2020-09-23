from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField


class TermCondition(models.Model):
    text = RichTextUploadingField()
    newest = models.BooleanField(
        default=False,
        help_text="If you accept it, these fields will be treated as valid terms&conditions for acceptance by users. The previous will be in the DB but not valid anymore",
    )
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Terms created at {self.created_at}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for term in TermCondition.objects.filter(newest=True).exclude(
            id=self.id
        ):
            term.newest = False
            term.save()
