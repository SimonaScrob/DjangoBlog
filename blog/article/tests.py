import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from article.models import Article
from user_auth.models import User


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'john%s' % n)
    email = factory.LazyAttribute(lambda o: '%s@example.com' % o.username)
    role = factory.Faker(
        'random_element', elements=[x[0] for x in User.ROLE_CHOICES]
    )


class ArticleFactory(factory.DjangoModelFactory):
    class Meta:
        model = Article

    title = factory.Sequence(lambda n: 'qqq%s' % n)
    content = u'ddffffgtrrdd tgrjmhmjhge fgrnghngege'
    author = factory.SubFactory(UserFactory)
    publication_date = factory.LazyFunction(datetime.datetime.now)


class TestArticleAPI(TestCase):
    def setUp(self):
        self.article = ArticleFactory()
        self.user = UserFactory()
        self.user.password = 'password'
        self.user.save()
        self.client = APIClient()

    def test_get_articles_not_logged(self):
        response = self.client.get(reverse("articles-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_articles_logged(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(reverse("articles-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
