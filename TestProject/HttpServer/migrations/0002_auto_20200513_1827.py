# Generated by Django 2.2.10 on 2020-05-13 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HttpServer', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='body',
            new_name='text',
        ),
        migrations.RemoveField(
            model_name='post',
            name='header',
        ),
    ]