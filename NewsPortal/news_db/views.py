from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)
from django.views.generic.edit import FormView
from .forms import PostForm
from .models import Post, Comment
from .filters import PostFilter

class PostsList(ListView):

    model = Post
    ordering = '-create_date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = PostFilter(self.request.get, queryset)
    #     return self.filterset.qs
    # 
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data()
    #     context['filterset'] = self.filterset
    #     return context
    
class PostsListFilter(ListView):

    model = Post
    ordering = '-create_date'
    template_name = 'post_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context

class PostDetails(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class NewsDetails(DetailView):
    model = Post
    queryset = Post.objects.filter(position="NW")
    template_name = 'post.html'
    context_object_name = 'post'
    
class ArticleDetails(DetailView):
    model = Post
    queryset = Post.objects.filter(position="AR")
    template_name = 'post.html'
    context_object_name = 'post'


class ArticlesList(ListView):
    model = Post
    queryset = Post.objects.filter(position="AR")
    ordering = '-create_date'
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 10

    
class NewsList(ListView):
    model = Post
    queryset = Post.objects.filter(position="NW")
    ordering = '-create_date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class NewsCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news_create.html'

    def form_valid(self, form):
        post  = form.save(commit=True)
        post.position = 'NW'
        return super().form_valid(form)
    
class ArticleCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'article_create.html'

class NewsEdit(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news_edit.html'

class ArticleEdit(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'article_edit.html'

class NewsDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('news_list')
    template_name = 'news_delete.html'
    
class ArticleDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('articles_list')
    template_name = 'article_delete.html'

# Create your views here.
