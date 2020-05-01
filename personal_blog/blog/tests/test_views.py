from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from blog.models import Post, Category


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = reverse("home")
        self.detail_url = reverse("post_detail", args=["pierwszy-post"])
        self.filter_post = reverse("filter_post")
        self.field_post = reverse("post_category", args=["python"])
        self.user = User(
            first_name="adam", is_staff=True, is_active=True, is_superuser=True
        )
        self.user.save()
        self.category = Category.objects.create(
            name="Python", is_active=True, slug="python"
        )
        self.category.save()
        self.post = Post.objects.create(
            field=self.category,
            title="Pierwszy post",
            slug="pierwszy-post",
            status=1,
            author=self.user,
        )
        self.post2 = Post.objects.create(
            field=self.category,
            title="Drugi post",
            slug="drugi-post",
            status=1,
            author=self.user,
        )

    def test_blog_list_GET(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/home.html")

    def test_blog_detail_GET(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_detail.html")
        self.assertIsNotNone(response.context["form"])

    def test_post_detail_POST(self):
        response = self.client.post(
            self.detail_url,
            {
                "post": Post.objects.get(title="Pierwszy post"),
                "author": "robot",
                "text": "ok",
            },
        )
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "robot - twój post został wysłany do zatwierdzenia przez administratora",
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_detail.html")
        self.assertEqual(self.post.comments.first().author, "robot")
        self.assertIsNotNone(response.context["form"])

    def test_post_detail_POST_nodata(self):
        response = self.client.post(self.detail_url)
        self.assertIsNotNone(response.context["form"])
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_detail.html")
        self.assertEqual(self.post.comments.count(), 0)

    def test_filter_post_GET(self):
        qs = Post.objects.filter(title="Drugi post")
        response = self.client.get(self.filter_post, {"q": "Drugi"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/filter_post.html")
        self.assertQuerysetEqual(
            response.context["object_list"], qs, transform=lambda x: x
        )
        self.assertEqual(response.context["object_list"].count(), 1)

    def test_field_post_GET(self):
        qs = Post.objects.filter(field__name="Python")
        response = self.client.get(self.field_post)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_category.html")
        self.assertQuerysetEqual(
            response.context["object_list"], qs, transform=lambda x: x
        )
        self.assertEqual(response.context["object_list"].count(), 2)

    def test_404(self):
        response = self.client.get('/404')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'blog/404.html')
        self.assertIn('404', response.content.decode('utf-8'))