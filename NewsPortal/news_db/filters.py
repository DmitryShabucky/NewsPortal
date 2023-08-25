from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter, CharFilter

from django import forms
from django.contrib.auth.models import User
from .models import Post, Category




class PostFilter(FilterSet):

    category = ModelMultipleChoiceFilter(
        field_name = 'category',
        queryset= Category.objects.all(),
        label = "Категория",
    )

    author = ModelMultipleChoiceFilter(
        field_name= 'author__user',
        queryset= User.objects.filter(author__isnull=False),
        label= 'Поиск по автору',
    )
    
    create_date = DateFilter(
        field_name= 'create_date',
        widget=forms.DateInput(attrs={'type':'date'}),
        lookup_expr='gt',
        label= 'Опубликовано после',
    )
   
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Поиск по заголовку'
    )
    
    class Meta():
        model = Post
        fields= ['category', 'title', 'author', 'create_date']

        
        
