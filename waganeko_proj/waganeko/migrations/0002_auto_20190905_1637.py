# Generated by Django 2.2.1 on 2019-09-05 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waganeko', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='prefer_book_category',
            field=models.IntegerField(choices=[(0, '小説'), (1, '科学')], null=True, verbose_name='好きな本のカテゴリ'),
        ),
    ]
