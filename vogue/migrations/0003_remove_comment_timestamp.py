# Generated by Django 3.0.8 on 2020-08-11 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vogue', '0002_comment_discussion_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='timestamp',
        ),
    ]
