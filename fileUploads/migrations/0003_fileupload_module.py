# Generated by Django 2.2.9 on 2020-07-22 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accountManagement', '0009_auto_20200718_1653'),
        ('fileUploads', '0002_auto_20200723_0352'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='module',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accountManagement.Module'),
            preserve_default=False,
        ),
    ]
