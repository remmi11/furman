# Generated by Django 2.0.7 on 2018-08-09 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_formall_volume'),
    ]

    operations = [
        migrations.AddField(
            model_name='formall',
            name='requested_by',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
