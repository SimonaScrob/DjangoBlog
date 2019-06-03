import datetime

from django.core.management import BaseCommand
from django.core.mail import send_mail, EmailMultiAlternatives

from article.models import Article


class Command(BaseCommand):

    def get_users_articles(self):
        users_emails = []
        articles = Article.objects.all().values("title", "publication_date", "author__email", "author__first_name")
        for article in articles:
            if article.get("publication_date") is not None:
                if (datetime.datetime.now().date() - article.get("publication_date")).days == 5 and \
                        article.get("author__email") is not None:
                    users_emails.append({"title": article.get("title"), "email_address": article.get("author__email"),
                                                                "name": article.get("author__first_name")})
        return users_emails

    # 5 days - the article was published - an email will be sent
    def send_email(self):
        send_details = self.get_users_articles()
        if send_details:
            for detail in send_details:
                subject = 'Alert'
                body = 'Hello {0}! 5 days passed since you published the artricle {1} '.format(detail["name"], detail["title"])
                from_email = 'simscrob@gmail.com'
                to_email = detail["email_address"]

                email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
                email_message.send()

    def handle(self, **options):
        self.send_email()
