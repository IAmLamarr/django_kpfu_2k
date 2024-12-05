# Generated by Django 5.1.3 on 2024-12-03 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_keyword_id_alter_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]