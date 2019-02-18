import django_filters

from article.models import Article


class ArticleFilter(django_filters.FilterSet):

    title = django_filters.CharFilter()
    author__first_name = django_filters.CharFilter(lookup_expr='icontains')
    publication_date = django_filters.DateFilter(field_name="publication_date", lookup_expr='lte')

    class Meta:
        model = Article
        exclude = ['author']
