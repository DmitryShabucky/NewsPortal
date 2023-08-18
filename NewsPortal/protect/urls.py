from django.urls import path

from news_db.views import IndexView

urlpatterns = [
    path('', IndexView.as_view()),
]