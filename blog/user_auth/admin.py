from django.contrib import admin

# Register your models here.
from article.models import Article, ArticleComment
from user_auth.models import User

admin.site.register(User)
admin.site.register(Article)
admin.site.register(ArticleComment)

