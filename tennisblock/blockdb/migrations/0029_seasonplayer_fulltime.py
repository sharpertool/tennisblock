# Generated by Django 3.0.11 on 2021-01-30 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockdb', '0028_auto_20191206_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='seasonplayer',
            name='fulltime',
            field=models.BooleanField(default=False),
        ),
    ]
