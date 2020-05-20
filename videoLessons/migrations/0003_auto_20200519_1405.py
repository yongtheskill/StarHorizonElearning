# Generated by Django 2.2.9 on 2020-05-19 06:05

import StarHorizonElearning.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoLessons', '0002_auto_20200518_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='afterAction',
            field=models.CharField(default='none', max_length=200, verbose_name='action to take after video'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='video',
            name='videoFile',
            field=models.FileField(default='', storage=StarHorizonElearning.storage_backends.MediaStorage(), upload_to=''),
            preserve_default=False,
        ),
    ]
