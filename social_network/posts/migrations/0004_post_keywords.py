# Generated by Django 5.1.3 on 2024-12-03 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_keyword_name_alter_post_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='keywords',
            field=models.ManyToManyField(to='posts.keyword'),
        ),
    ]