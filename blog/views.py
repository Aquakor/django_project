from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponse
from .models import Post


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # Override form_valid method so we can add an author to the Post
    # before commiting it to the database.
    def form_valid(self, form):
        # Take the instance and set the author to the current logged in user.
        form.instance.author = self.request.user
        # Run the parent class's form_valid
        # method and pass the updated argument.
        return super().form_valid(form)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
