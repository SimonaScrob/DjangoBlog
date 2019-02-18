from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from article.filters import ArticleFilter
from article.models import Article, ArticleComment
from article.pagination import ArticlePagination
from article.serializers import ArticleListSerializer, ArticleCRUDSerializer, ArticleCommentListSerializer, \
    ArticleCommentCRUDSerializer
# from user_auth.permissions import UserPermission
from user_auth.permissions import IsAllowedToCRUDComments
import django_filters.rest_framework


class ArticleView(viewsets.ModelViewSet):
    # serializer_class = ArticleSerializer
    # permission_classes = (IsAuthenticated, )
    # queryset = Article.objects.all()
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = ArticleFilter
    pagination_class = ArticlePagination
    ordering = ('title', )

    def create(self, request, *args, **kwargs):
        if request.data.get("author") is not None:
            return Response({'ha haa': 'no no no'},
                            status=status.HTTP_400_BAD_REQUEST)
        return super(ArticleView, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleCRUDSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_queryset(self):
        current_user = self.request.user
        if not current_user.is_admin:
            return Article.objects.filter(author__id=current_user.id)
        return Article.objects.all()

    def update(self, request, *args, **kwargs):
        article_pk = kwargs.get("pk")
        article = Article.objects.filter(id=article_pk).first()
        if article:
            author_id = article.id
        else:
            author_id = None
        if request.user.id != author_id:
            return Response({'hmmm': 'modify your own article! :p'},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super(ArticleView, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        article_pk = kwargs.get("pk")
        article = Article.objects.filter(id=article_pk).first()
        if article:
            author_id = article.author.id
        else:
            author_id = None
        if request.user.id != author_id:
            return Response({'hmmm': 'you have not permission to perform this operation'},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super(ArticleView, self).destroy(request, *args, **kwargs)


class ArticleCommentView(viewsets.ModelViewSet):
    queryset = ArticleComment.objects.all()
    # serializer_class = ArticleCommentSerializer
    permission_classes = (IsAllowedToCRUDComments, IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        if request.data.get("owner") is not None:
            return Response({'ha haa': 'no no no'},
                            status=status.HTTP_400_BAD_REQUEST)
        return super(ArticleCommentView, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleCommentListSerializer
        return ArticleCommentCRUDSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def update(self, request, *args, **kwargs):
        comment_pk = kwargs.get("pk")
        comment = ArticleComment.objects.filter(id=comment_pk).first()
        if comment:
            owner_id = comment.owner.id
        else:
            owner_id = None
        if request.user.id != owner_id:
            return Response({'hmmm': 'you have not permission to perform this operation'},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super(ArticleCommentView, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        comment_pk = kwargs.get("pk")
        comment = ArticleCommentView.objects.filter(id=comment_pk).first()
        if comment:
            owner_id = comment.author.id
        else:
            owner_id = None
        if request.user.id != owner_id:
            return Response({'hmmm': 'you have not permission to perform this operation'},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super(ArticleCommentView, self).destroy(request, *args, **kwargs)

