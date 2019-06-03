from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from article.views import ArticleView, ArticleCommentView
from user_auth.views import UserView

schema_view = get_swagger_view(title='Blog')


urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^admin/', admin.site.urls),
    url(r'', include("user_auth.urls")),  # users API endpoints
    url(r'^swagger/', schema_view),
    url(r'^accounts/', include('allauth.urls')),

]

router = DefaultRouter()

router.register(r'articles', ArticleView, base_name='articles')
router.register(r'comments', ArticleCommentView, base_name='comments')
router.register(r'users', UserView, base_name='users')

urlpatterns += router.urls
