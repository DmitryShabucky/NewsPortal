from django.urls import path
from .views import PostsList, PostDetails, PostCreate

urlpatterns = [
    path('', PostsList.as_view(), name= 'posts_list'),
    path('<int:pk>', PostDetails.as_view(), name= 'post_details'),
    path('create/', PostCreate.as_view(), name= "post_create"),
]