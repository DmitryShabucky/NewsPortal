from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .management.commands.runapscheduler import my_job


@shared_task
def weekly_news_email_send():
    my_job()

@shared_task
def send_notifications(preview, pk, position, title, subscribers):
    if position == "NW":
        html_content = render_to_string(
            'user/post_created_email.html',
            {
                'text': preview,
                'link': f'{settings.STATIC_URL}/news/{pk}',
            }
        )
    else:
        html_content = render_to_string(
            'user/post_created_email.html',
            {
                'text': preview,
                'link': f'{settings.STATIC_URL}/articles/{pk}',
            }
        )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
