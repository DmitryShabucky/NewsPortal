# Generated by Django 4.2.4 on 2023-08-20 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news_db', '0003_alter_comment_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcategory',
            name='subscribers',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
