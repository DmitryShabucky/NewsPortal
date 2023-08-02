from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Comment

class PostsList(ListView):

    model = Post
    ordering = '-create_date'
    template_name = 'posts.html'
    context_object_name = 'posts'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data()
    #     context['posts_total'] = None
    #     return context

class PostDetails(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
# Create your views here.
