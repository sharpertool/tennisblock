# Generated by Django 2.0.8 on 2018-09-21 02:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blockdb', '0004_auto_20180915_1815'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='season',
        ),
    ]
