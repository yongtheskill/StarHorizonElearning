# Generated by Django 2.2.9 on 2020-07-22 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fileUploads', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fileupload',
            old_name='filID',
            new_name='fileID',
        ),
    ]
