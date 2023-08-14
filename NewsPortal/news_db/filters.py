from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter, CharFilter, DateFromToRangeFilter

from django_filters.widgets import DateRangeWidget
from django_filters import widgets

from django.contrib.auth.models import User
from .models import Post


class PostFilter(FilterSet):

    author = ModelMultipleChoiceFilter(
        field_name= 'author__user',
        queryset= User.objects.filter(author__isnull=False),
        label= 'Автор',
        conjoined= False,
    )
    create_date = DateFromToRangeFilter(
        field_name='create_date',
        lookup_expr='gt',
        label='Опубликовано после',
        widget=DateRangeWidget(attrs={'placeholder': 'YYYY/MM/DD'})
    )
    # create_date = DateFilter(
    #     field_name='create_date',
    #     lookup_expr='gt',
    #     label= 'Опубликовано после',
    # )
   
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Слово'
    )
    
    class Meta():
        model = Post
        fields= ['author', 'create_date', 'title']
        
