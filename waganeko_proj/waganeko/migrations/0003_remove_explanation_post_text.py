# Generated by Django 2.2.4 on 2019-09-09 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waganeko', '0002_explanation_tweet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='explanation',
            name='post_text',
        ),
    ]
