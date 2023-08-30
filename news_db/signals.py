from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings

from news_db.models import PostCategory, Post
from .tasks import send_notifications




# def send_notifications(preview, pk, position, title, subscribers):
#     if position == "NW":
#         html_content = render_to_string(
#             'user/post_created_email.html',
#             {
#                 'text': preview,
#                 'link': f'{settings.STATIC_URL}/news/{pk}',
#             }
#         )
#     else:
#         html_content = render_to_string(
#             'user/post_created_email.html',
#             {
#                 'text': preview,
#                 'link': f'{settings.STATIC_URL}/articles/{pk}',
#             }
#         )
#
#     msg = EmailMultiAlternatives(
#         subject=title,
#         body='',
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=subscribers,
#     )
#
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_the_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers = []
        subscribers_emails = []
        for cat in categories:
            subscribers += cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        # send_notifications(instance.preview(), instance.pk, instance.position, instance.title, subscribers_emails)
        send_notifications.delay(instance.preview(), instance.pk, instance.position, instance.title, subscribers_emails)

@receiver(pre_save, sender=Post)
def day_posts_limit(sender, instance, **kwargs):
    user = instance.author.user
    today = timezone.now().date()
    count = Post.objects.filter(author__user=user, create_date__date=today).count()

    if count > 3:
        raise ValueError('Вы не можете создать больше трех статей в сутки.')

