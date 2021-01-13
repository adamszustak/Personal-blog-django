from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView, View

from comments.forms import CommentForm
from conf.utils import render_to_pdf
from taggit.models import Tag

from .models import Category, Post


def post_list(request, category_slug=None, tag_slug=None):
    posts = Post.published.all()
    context = {}
    query = request.GET.get("q")
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = Post.published.filter(field=category)
        context["object"] = category
    elif tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.published.filter(tags__slug=tag.slug)
        context["object"] = tag
    elif query:
        posts = Post.published.filter(
            Q(field__name__icontains=query) | Q(title__icontains=query)
        )
    paginator = Paginator(posts, 6)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse("")
        posts = paginator.page(paginator.num_pages)
    context["object_list"] = posts
    if request.is_ajax():
        return render(request, "blog/snippets/_posts.html", context)
    return render(request, "blog/home.html", context)


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context["form"] = CommentForm
        self.one_post = get_object_or_404(Post, slug=self.kwargs["slug"])
        comments = cache.get("comments")
        print(comments)
        if not comments:
            comments = self.one_post.comments.filter(is_approved=True)
            cache.set("comments", comments)
        context["comments"] = comments
        context["tags"] = self.one_post.tags.all()
        recomended_posts = self.one_post.recomended_posts()
        context["recomended_posts"] = recomended_posts
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
    return render(request, "404.html", status=404)
