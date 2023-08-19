from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView,
)
# from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


from .forms import PostForm
from .models import Post, Author
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


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news_db.add_post',)
    model = Post
    form_class = PostForm
    template_name = 'news_create.html'

    def form_valid(self, form):
        post  = form.save(commit=True)
        post.position = 'NW'
        return super().form_valid(form)
    
class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news_db.add_post',)
    model = Post
    form_class = PostForm
    template_name = 'article_create.html'

class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news_db.change_post',)
    model = Post
    form_class = PostForm
    template_name = 'news_edit.html'

class ArticleEdit(PermissionRequiredMixin,UpdateView):
    permission_required = ('news_db.change_post',)
    model = Post
    form_class = PostForm
    template_name = 'article_edit.html'

class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news_db.delete_post',)
    model = Post
    success_url = reverse_lazy('news_list')
    template_name = 'news_delete.html'
    
class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news_db.delete_post',)
    model = Post
    success_url = reverse_lazy('articles_list')
    template_name = 'article_delete.html'

@login_required
def author_me(request):

    user = request.user
    author_group = Group.objects.get(name= 'author')
    if not request.user.groups.filter(name= 'author').exists():
        author_group.user_set.add(user)
    return redirect('/')




