# Generated by Django 2.2.4 on 2019-09-11 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waganeko', '0012_explanation_total_nums'),
    ]

    operations = [
        migrations.AlterField(
            model_name='explanation',
            name='tweet',
            field=models.TextField(default='', verbose_name='ツイート'),
        ),
    ]
