# Generated by Django 2.2.4 on 2019-09-11 01:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blockdb', '0016_auto_20190907_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduleverify',
            name='code',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='scheduleverify',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
