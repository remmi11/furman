# Generated by Django 2.0.7 on 2019-01-07 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20190104_1441'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formall',
            name='country',
        ),
    ]
