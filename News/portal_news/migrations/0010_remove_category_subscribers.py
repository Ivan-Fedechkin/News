# Generated by Django 4.0.5 on 2022-11-01 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal_news', '0009_delete_appointment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='subscribers',
        ),
    ]
