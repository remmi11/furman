# Generated by Django 2.0.7 on 2018-08-10 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_formall_requested_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='formall',
            name='well_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='formall',
            name='well_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
