# Generated by Django 4.2.5 on 2023-09-05 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sending_app', '0004_token_chat_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='subscribed',
            field=models.BooleanField(default=False),
        ),
    ]
