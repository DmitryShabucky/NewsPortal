from .celery import app as celery_app, app
from celery.schedules import crontab

__all__ = ('celery_app',)

app.conf.beat_schedule = {
    'email_every_monday_8am': {
        'task': 'news_db.tasks.weekly_news_email_send',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}