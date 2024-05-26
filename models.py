from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self, post_rating = None):
        author_posts_rating = Post.objects.filter(author_id=self.pk).aggregate(
            post_rating_sum=Coalesce(Sum('rating_post') * 3, 0)
        )
        author_comments_rating = Comment.objects.filter(user_id = self.user).aggregate(
            comment_rating_sum=Coalesce(Sum('rating_comment'), 0)
        )
        author_post_comments_rating = Comment.objects.filter(post__author__name=self.user).aggregate(
            comment_rating_sum = Coalesce(Sum('rating_comment'), 0))

        author_rating = post_rating + author_comments_rating + author_post_comments_rating
        self.rating_author = author_posts_rating['post_rating_sum'] + author_comments_rating['comment_rating_sum'] + author_post_comments_rating['comment_rating_sum']
        self.save()

    pass

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    pass

class Post(models.Model):

    news = "NA"
    articles = "AR"

    POST_TYPES = [
        (news, "Новость"),
        (articles, "Статья")
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    poste_type = models.IntegerField(max_length=10, default=0)
    date_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def preview(self):
        return f"{self.text[:124]}..."

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    text = models.TextField()
    date_in = models.DateTimeField(auto_now_add=True)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()