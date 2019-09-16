# Generated by Django 2.2.4 on 2019-09-16 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blockdb', '0023_auto_20190914_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduleverify',
            name='sent_to',
            field=models.EmailField(blank=True, max_length=254, verbose_name='send email address'),
        ),
        migrations.AlterUniqueTogether(
            name='scheduleverify',
            unique_together=set(),
        ),
    ]
