from rest_framework import serializers

from article.models import Article, ArticleComment


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("pk", "title", "content", "author", "publication_date")


class ArticleCRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("title", "content")


class ArticleCommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = ("id", "content", "owner", "article")


class ArticleCommentCRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = ("content", "article")


class ArticleCommentSerializer(serializers.ModelSerializer):
    comments = ArticleCommentListSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = ("pk", "title", "content", "author", "publication_date", "comments")
