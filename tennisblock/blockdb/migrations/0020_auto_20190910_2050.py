# Generated by Django 2.2.4 on 2019-09-11 01:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blockdb', '0019_auto_20190910_2048'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='scheduleverify',
            unique_together={('schedule', 'email')},
        ),
    ]
