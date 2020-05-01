from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib import messages

from comments.forms import CommentForm
from .models import Post, Category


class PostList(ListView):
    model = Post
    paginate_by = 9
    template_name = "blog/home.html"
    queryset = Post.published.all()


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context["form"] = CommentForm
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
            context["form"] = form
            return self.render_to_response(context=context)


class PostFilterList(ListView):
    model = Post
    paginate_by = 9
    template_name = "blog/filter_post.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Post.published.filter(
            Q(field__name__icontains=query) | Q(title__icontains=query)
        )
        return object_list


class PostFieldView(ListView):
    model = Post
    paginate_by = 9
    template_name = "blog/post_category.html"

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return Post.published.filter(field=self.category)

    def get_context_data(self, **kwargs):
        context = super(PostFieldView, self).get_context_data(**kwargs)
        context["category"] = self.category
        return context


def error_404(request, exception):
    return render(request, 'blog/404.html', status=404)