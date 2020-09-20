from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from taggit.models import Tag

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.template.loader import get_template
from django.conf import settings
from django.db.models import Q

from comments.forms import CommentForm
from .models import Post, Category
from conf.utils import render_to_pdf


class PostList(ListView):
    model = Post
    paginate_by = 9
    template_name = "blog/home.html"
    queryset = Post.published.all()


class PostFilterList(ListView):
    model = Post
    paginate_by = 9
    template_name = "blog/home.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Post.published.filter(
            Q(field__name__icontains=query) | Q(title__icontains=query)
        )
        return object_list


class PostCategoryView(ListView):
    model = Post
    paginate_by = 9
    template_name = "blog/home.html"

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return Post.published.filter(field=self.category)

    def get_context_data(self, **kwargs):
        context = super(PostCategoryView, self).get_context_data(**kwargs)
        context["object"] = self.category
        return context


class PostTagView(ListView):
    model = Post
    paginate_by = 9
    template_name = "blog/home.html"

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs["slug"])
        return Post.published.filter(tags__slug=self.tag.slug)

    def get_context_data(self, **kwargs):
        context = super(PostTagView, self).get_context_data(**kwargs)
        context["object"] = self.tag
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context["form"] = CommentForm
        self.one_post = get_object_or_404(Post, slug=self.kwargs["slug"])
        context["comments"] = self.one_post.comments.filter(is_approved=True)
        context["tags"] = self.one_post.tags.all()
        context["recomended_posts"] = self.one_post.recomended_posts()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            self.object = self.get_object()
            post = get_object_or_404(Post, slug=self.object.slug)
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            username = form.cleaned_data.get("author")
            messages.success(
                request,
                f"{username} - twój post został wysłany do zatwierdzenia przez administratora",
            )
            context = super(PostDetailView, self).get_context_data(**kwargs)
            context["form"] = CommentForm
            return self.render_to_response(context=context)
        else:
            self.object = self.get_object()
            context = super(PostDetailView, self).get_context_data(**kwargs)
            context["form"] = CommentForm()
            return self.render_to_response(context=context)


class HtmlToPdfView(View):
    def get(self, request, *args, **kwargs):
        self.one_post = get_object_or_404(Post, slug=self.kwargs["slug"])
        context = {"post": self.one_post}
        pdf = render_to_pdf("pdf.html", context)
        response = HttpResponse(pdf, content_type="application/pdf")
        response[
            "Content-Disposition"
        ] = f'inline; filename="{settings.BLOG_TITLE} - {self.one_post.title}.pdf"'
        return response


def error_404(request, exception):
    return render(request, "blog/404.html", status=404)
