from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_user = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user}'

    def update_rating(self):
        rating_post_author = self.post_set.all().aggregate(Sum('rating_post'))['rating_post__sum']
        rating_comment = self.user.comment_set.all().aggregate(Sum('rating_comment'))['rating_comment__sum']
        rating_comment_post = Comment.objects.filter(post__author__pk=self.pk).aggregate(Sum('rating_comment'))[
            'rating_comment__sum']
        self.rating_user = rating_post_author * 3 + rating_comment + rating_comment_post
        self.save()

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

class Post(models.Model):
    article = 'AR'
    news = 'NE'
    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новость')
    ]
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    select_choices = models.CharField(max_length=2, choices=POSITIONS, default=news)
    time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    heading_post = models.CharField(max_length=100)
    text_post = models.TextField()
    rating_post = models.IntegerField(default=0)

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return self.text_post[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.CharField(max_length=255)
    time_in = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()


