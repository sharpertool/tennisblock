# Generated by Django 2.1.2 on 2018-10-26 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockdb', '0006_auto_20180920_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='court_count',
            field=models.IntegerField(null=True),
        ),
    ]
