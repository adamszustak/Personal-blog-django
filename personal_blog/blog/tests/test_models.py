from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

from blog.models import Post, Category


class PostModelTest(TestCase):
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
        Post.objects.create(
            field=cls.category,
            title="Pierwszy post",
            slug="pierwszy-post",
            status=1,
        )

    def setUp(self):
        self.post = Post.objects.get(title="Pierwszy post")
        self.user = User.objects.get(first_name="adam")

    def test_default_author(self):
        self.assertEquals(self.post.author.first_name, self.user.first_name)

    def test_str(self):
        self.assertEquals(self.post.title, str(self.post))

    def test_get_absolute_url(self):
        self.assertEquals(self.post.get_absolute_url(), "/pierwszy-post")

    def test_img_url(self):
        self.assertEquals(self.post.img.url, self.post.img_url)

    def test_published_manager(self):
        self.assertEquals(Post.published.all().count(), 1)

        self.post.status = 0
        self.post.save()
        self.assertEquals(Post.published.all().count(), 0)

    def test_taggable_manager(self):
        self.post.tags.add("apple, ball cat dog")
        tags = [str(x) for x in self.post.tags.all()]
        self.assertEqual(tags, ["apple, ball cat dog"])


class TestCategoryModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name="Python", is_active=True, slug="python"
        )

    def setUp(self):
        self.category = Category.objects.get(id=2)

    def test_str(self):
        self.assertEquals(self.category.name, str(self.category))

    def test_get_absolute_url(self):
        self.assertEquals(self.category.get_absolute_url(), "/category/python")
