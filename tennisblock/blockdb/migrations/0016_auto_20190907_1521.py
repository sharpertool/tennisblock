# Generated by Django 2.2.4 on 2019-09-07 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blockdb', '0015_auto_20190907_1217'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='schedule',
            unique_together={('meeting', 'player')},
        ),
    ]
