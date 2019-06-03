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
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("articles-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_article(self):
        self.client.force_authenticate(user=self.user)
        articles_before = Article.objects.count()
        data = {"title": "lol",
                "content": "lol",
                }
        response = self.client.post(reverse("articles-list"), data=data)
        articles_after = Article.objects.count()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(articles_after - articles_before == 1)

    def test_delete_article(self):
        self.client.force_authenticate(user=self.user)
        articles_before = Article.objects.count()
        data = {"title": "loll",
                "content": "loll",
                }
        self.client.post(reverse("articles-list"), data=data)
        item_id = Article.objects.get(title=data["title"]).id
        response = self.client.delete(reverse("articles-detail", args=[item_id, ]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        articles_after = Article.objects.count()
        self.assertTrue(articles_after - articles_before == 0)


    def test_update_article(self):
        self.client.force_authenticate(user=self.user)
        data = {"title": "loll",
                "content": "loll",
                }
        resp = self.client.post(reverse("articles-list"), data=data)
        item_id = Article.objects.get(title=data["title"]).id
        data_patch = {"content": "updated"}
        self.assertFalse(resp.data["content"] == data_patch["content"])
        response = self.client.patch(reverse("articles-detail", args=[item_id, ]), data=data_patch)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], data_patch["content"])


class TestCommentsAPI(TestCase):
    def setUp(self):
        self.article = ArticleFactory()
        self.user = UserFactory()
        self.user.password = 'password'
        self.user.save()
        self.client = APIClient()

    def test_get_comments(self):
        pass