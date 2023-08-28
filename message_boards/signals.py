from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Advertsement, Category, Replies, News
from sign.models import MyUser


@receiver(post_save, sender=News)
def news_save(sender, instance, **kwargs):
    users = MyUser.objects.all()
    emails = [user.email for user in users]
    html_content = render_to_string(
        'message_boards/email_news.html',
        {},
            )
    msg = EmailMultiAlternatives(
        subject='Новость',
        body=f"Привет - {instance.body}",
        from_email='Lafen55@yandex.ru',
        to=emails,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(post_save, sender=Replies)
def post_save(sender, instance, **kwargs):
    user_advertsement_id = MyUser.objects.get(id=instance.advertsement.user_id)
    current_user = MyUser.objects.get(id=instance.user_id)
    advertsement = Advertsement.objects.get(id=instance.advertsement_id)
    user_advertsement = MyUser.objects.get(id=user_advertsement_id.id)
    html_content = render_to_string(
        'message_boards/email_reply.html',
        {'reply': instance,
         'advertsement': advertsement,
         'user_advertsement': user_advertsement
         }
    )
    msg = EmailMultiAlternatives(
        subject={instance.body},
        body=f"Новый отклик от {user_advertsement_id}",
        from_email='Lafen55@yandex.ru',
        to=[current_user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

