# Generated by Django 2.0.7 on 2019-01-04 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20180928_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formall',
            name='date_needed',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
