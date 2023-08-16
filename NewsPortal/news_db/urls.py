from django.urls import path
from .views import (
    PostsList, PostDetails, PostsListFilter, ArticlesList, NewsList, NewsCreate, ArticleCreate, 
    NewsDetails, ArticleDetails, NewsEdit, ArticleEdit, NewsDelete, ArticleDelete
)


urlpatterns = [
    path('', PostsList.as_view(), name= 'post_list'),
    path('<int:pk>', PostDetails.as_view(), name= 'post_details'),
    path('search/', PostsListFilter.as_view(), name= 'post_list_filter'),
    path('news/', NewsList.as_view(), name= 'news_list'),
    path('articles/', ArticlesList.as_view(), name= 'articles_list'),
    path('news/create/', NewsCreate.as_view(), name= 'news_create'),
    path('articles/create/', ArticleCreate.as_view(), name= 'article_create'),
    path('news/<int:pk>', NewsDetails.as_view(), name= 'news_details'),
    path('articles/<int:pk>', ArticleDetails.as_view(), name= 'article_details'),
    path('news/<int:pk>/edit/', NewsEdit.as_view(), name= 'news_edit'),
    path('articles/<int:pk>/edit/', ArticleEdit.as_view(), name= 'article_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name= 'news_delete'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name= 'article_delete'),
]