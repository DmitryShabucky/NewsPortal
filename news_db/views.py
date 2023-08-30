
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView,
)

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .forms import PostForm
from .models import Post, Category
from .filters import PostFilter


class PostsList(ListView):
    model = Post
    ordering = '-create_date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author']= not self.request.user.groups.filter(name= 'author').exists()
        return context


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
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class PostDetails(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author']= not self.request.user.groups.filter(name= 'author').exists()
        return context


class NewsDetails(DetailView):
    model = Post
    queryset = Post.objects.filter(position="NW")
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author']= not self.request.user.groups.filter(name= 'author').exists()
        return context

class ArticleDetails(DetailView):
    model = Post
    queryset = Post.objects.filter(position="AR")
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author']= not self.request.user.groups.filter(name= 'author').exists()
        return context


class ArticlesList(ListView):
    model = Post
    queryset = Post.objects.filter(position="AR")
    ordering = '-create_date'
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author']= not self.request.user.groups.filter(name= 'author').exists()
        return context


class NewsList(ListView):
    model = Post
    queryset = Post.objects.filter(position="NW")
    ordering = '-create_date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author']= not self.request.user.groups.filter(name= 'author').exists()
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news_db.add_post',)
    model = Post
    form_class = PostForm
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=True)
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


class ArticleEdit(PermissionRequiredMixin, UpdateView):
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

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author']= not self.request.user.groups.filter(name= 'author').exists()
        return context


@login_required
def author_me(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
    return redirect('newsportal/')


class CategoryListView(PostsList):
    model = Post
    template_name = 'category/category_list.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category = self.category).order_by('-create_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        context['is_not_subscribed'] = self.request.user not in self.category.subscribers.all()
        context['is_subscribed'] = self.request.user in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы подписались на рассылку новостей категории'
    return render(request, 'category/subscribe.html', {'category':category, 'message':message})


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)

    message = 'Вы отписались от рассылки новостей категории'
    return render(request, 'category/unsubscribe.html', {'category': category, 'message': message})
