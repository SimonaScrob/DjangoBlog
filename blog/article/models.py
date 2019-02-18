from django.db import models

from user_auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, related_name="articles", on_delete=models.CASCADE, null=True)
    publication_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class ArticleComment(models.Model):
    content = models.TextField()
    article = models.ForeignKey(Article, related_name="comments", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return self.owner.username + " - " + self.article.title

