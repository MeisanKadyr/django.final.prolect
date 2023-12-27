# Generated by Django 5.0 on 2023-12-26 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photoapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='submitter',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='created',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='description',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='title',
        ),
    ]
