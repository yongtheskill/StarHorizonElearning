# Generated by Django 2.2.9 on 2020-09-06 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountManagement', '0013_auto_20200815_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='courseCode',
            field=models.CharField(max_length=200, null=True, verbose_name='course code'),
        ),
    ]