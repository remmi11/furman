# Generated by Django 2.0.7 on 2019-04-25 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_auto_20190406_0439'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickets',
            name='account_no',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tickets',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]