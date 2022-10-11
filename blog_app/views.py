from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, View, TemplateView, DeleteView
from blog_app.models import Blog, Comment, Likes
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
from .forms import CommentForm
# Create your views here.


class MyBlogs(LoginRequiredMixin, TemplateView):
    template_name = 'blog_app/my_blog.html'


class EditBlog(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ('blog_title', 'blog_content', 'blog_img')
    template_name = 'blog_app/edit_blog.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('blog_app:blog_detail', kwargs={'slug': self.object.slug})


class CreateBlog(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'blog_app/create_blog.html'
    fields = ('blog_title', 'blog_content', 'blog_img')

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        title = blog_obj.blog_title
        blog_obj.slug = title.replace(' ', '-') + '-' + str(uuid.uuid4())
        blog_obj.save()
        return HttpResponseRedirect(reverse('blog_app:blog_list'))


class BlogList(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'blog_app/blog_list.html'
    # queryset = Blog.objects.order_by('-publish_date')


@login_required
def blog_detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    form = CommentForm()
    already_liked = Likes.objects.filter(blog=blog, user=request.user)
    if already_liked:
        liked = True
    else:
        liked = False

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('blog_app:blog_detail', kwargs={'slug': slug}))

    return render(request, 'blog_app/blog_details.html', context={'blog': blog, 'form': form, 'liked': liked})


@login_required
def liked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user

    already_liked = Likes.objects.filter(blog=blog, user=user)
    if not already_liked:
        liked_post = Likes(blog=blog, user=user)
        liked_post.save()
    return HttpResponseRedirect(reverse('blog_app:blog_detail', kwargs={'slug': blog.slug}))


@login_required
def unliked(request, pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user

    already_liked = Likes.objects.filter(blog=blog, user=user)
    already_liked.delete()

    return HttpResponseRedirect(reverse('blog_app:blog_detail', kwargs={'slug': blog.slug}))
