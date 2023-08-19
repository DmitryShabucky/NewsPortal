from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter, CharFilter

from django import forms
from django.contrib.auth.models import User
from .models import Post




class PostFilter(FilterSet):

    author = ModelMultipleChoiceFilter(
        field_name= 'author__user',
        queryset= User.objects.filter(author__isnull=False),
        label= 'Поиск по автору',
        conjoined= False,
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
        fields= [ 'title', 'author', 'create_date']

        
        
