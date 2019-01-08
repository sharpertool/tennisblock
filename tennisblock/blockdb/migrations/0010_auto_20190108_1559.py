# Generated by Django 2.1.5 on 2019-01-08 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blockdb', '0009_auto_20190105_1930'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleVerify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_created=True)),
                ('code', models.UUIDField()),
                ('confirmation_type', models.CharField(choices=[('C', 'Confirm'), ('R', 'Reject'), ('A', 'Awaiting Response')], default='A', max_length=1)),
            ],
        ),
        migrations.AddField(
            model_name='schedule',
            name='confirmation_status',
            field=models.CharField(choices=[('A', 'Awaiting Response'), ('C', 'Schedule Confirmed'), ('R', 'Scheduled but not available'), ('U', 'Unconfirmed')], default='U', max_length=2),
        ),
        migrations.AddField(
            model_name='scheduleverify',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blockdb.Schedule'),
        ),
    ]
