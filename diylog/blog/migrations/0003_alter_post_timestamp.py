# Generated by Django 4.0.6 on 2022-07-28 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='timeStamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
