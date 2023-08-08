from django_filters import FilterSet, ModelChoiceFilter
from h11._abnf import field_name

from  .models import Post, Category

Category = ModelChoiceFilter(
    field_name= 'product_category__category',
    queryset=Category.objects.all(),
    lable='Category',
    empty_lable= 'any',
)
class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {}