import logging
from datetime import datetime, timedelta

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news_db.models import Category, Post

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    date = datetime.utcnow() - timedelta(days=7)
    subscribers = Category.subscribers.all()
    user_posts = {}

    for subscriber in subscribers:
        email = subscriber.email
        subscriber_categories = list(subscriber.categories.values_list('name', flat=True))
        subscribed_posts = []
        for s_c in subscriber_categories:
            subscribed_posts += Post.objects.filter(category=s_c, create_date__gt=date)
        user_posts[email] = subscribed_posts

    for email, posts in user_posts.items():
        html_content = render_to_string(
            'user/weekly_subscribers_mails.html',
            {
                'posts': posts,
                'link': f'{settings.STATIC_URL}/',
            }
        )

        msg = EmailMultiAlternatives(
            subject='Your favorite weekly news.',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=email
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(week="*/1"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="fri", hour="11", minute="15"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
