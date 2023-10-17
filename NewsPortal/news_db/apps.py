from django.apps import AppConfig


class NewsDbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news_db'

    def ready(self):
        import news_db.signals