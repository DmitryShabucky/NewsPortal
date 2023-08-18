from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import CommonRegisterView
from news_db.views import author_me

urlpatterns = [
    path('login/', LoginView.as_view(template_name='sign/login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'),
         name='logout'),
    path('signup/', CommonRegisterView.as_view(template_name='sign/signup.html'),
         name='signup'),
    path('author/', author_me, name= 'author_me'),
]
