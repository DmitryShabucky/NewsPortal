from django.core.cache import cache

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)

    def update_rating(self):
        post_rateing = Post.objects.filter(author=self).aggregate(pr=Coalesce(Sum('rate'),
                                                                              0))['pr']
        comments_raiting = Comment.objects.filter(user=self.user).aggregate(cr=Coalesce(Sum('rate'),
                                                                                        0))['cr']
        all_posts_rating = Comment.objects.filter(post__author=self).aggregate(apr=Coalesce(Sum('rate'),
                                                                                            0))['apr']

        self.rate = post_rateing * 3 + comments_raiting + all_posts_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    article = 'AR'
    news = 'NW'

    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новость')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    position = models.CharField(max_length=2, choices=POSITIONS, default=article)
    create_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=250)
    text = models.TextField()
    rate = models.IntegerField(default=0)

    category = models.ManyToManyField(Category, through='PostCategory')

    def __str__(self):
        return f"{self.get_position_display()}: {self.title}. Дата публикации: {self.create_date.date()}. {self.text}"

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()

    def preview(self):
        return f"{self.text[:125:]}..."

    def get_absolute_url(self):
        return reverse('post_details', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post - {self.pk}')

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)

    def __str__(self):
        return self.text

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()



