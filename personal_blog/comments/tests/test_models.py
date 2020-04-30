from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings

from blog.models import Post, Category
from comments.models import Comment, ReplyComment


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User(
            first_name="adam",
            is_staff=True,
            is_active=True,
            is_superuser=True,
            email=settings.DEFAULTUSERMAIL,
        )
        cls.user.save()
        cls.category = Category.objects.create(name="Python", is_active=True)
        cls.category.save()
        cls.post = Post.objects.create(
            field=cls.category,
            title="Pierwszy post",
            slug="pierwszy-post",
            status=1,
        )
        cls.post.save()
        Comment.objects.create(
            post=Post.objects.get(id=1), author="robot", text="ok"
        )

    def setUp(self):
        self.post = Post.objects.get(id=1)
        self.comment = Comment.objects.get(id=1)

    def test_str(self):
        self.assertEqual(self.comment.text, "ok")

    def test_approve(self):
        self.assertIs(self.comment.is_approved, False)
        self.comment.is_approved = True
        self.assertIs(self.comment.is_approved, True)


class ReplyCommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User(
            first_name="adam",
            is_staff=True,
            is_active=True,
            is_superuser=True,
            email=settings.DEFAULTUSERMAIL,
        )
        cls.user.save()
        cls.category = Category.objects.create(name="Python", is_active=True)
        cls.category.save()
        cls.post = Post.objects.create(
            field=cls.category,
            title="Pierwszy post",
            slug="pierwszy-post",
            status=1,
            author=cls.user,
        )
        cls.post.save()
        cls.comment = Comment.objects.create(
            post=Post.objects.get(id=2), author="robot", text="ok"
        )
        cls.comment.save()
        ReplyComment.objects.create(
            comment=Comment.objects.get(id=2), text="not ok", author=cls.user,
        )

    def setUp(self):
        self.post = Post.objects.get(id=2)
        self.comment = Comment.objects.get(id=2)
        self.reply = ReplyComment.objects.get(id=1)

    def test_str(self):
        self.assertEqual(self.reply.text, "not ok")
