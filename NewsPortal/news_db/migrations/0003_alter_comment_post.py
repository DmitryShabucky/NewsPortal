# Generated by Django 4.2.3 on 2023-08-01 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news_db', '0002_alter_author_rate_alter_comment_rate_alter_post_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='news_db.post'),
        ),
    ]
