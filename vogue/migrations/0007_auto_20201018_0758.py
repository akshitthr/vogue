# Generated by Django 3.1.2 on 2020-10-18 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vogue', '0006_discussionfollow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
