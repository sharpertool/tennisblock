# Generated by Django 2.0.8 on 2018-09-15 23:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tennis_profile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tennisuser',
            name='spouse',
        ),
        migrations.RemoveField(
            model_name='tennisuser',
            name='user',
        ),
        migrations.DeleteModel(
            name='TennisUser',
        ),
    ]
