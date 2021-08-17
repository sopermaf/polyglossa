# Generated by Django 3.0.4 on 2020-08-30 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class_bookings', '0003_auto_20200627_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='is_highlighted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='activity',
            name='order_shown',
            field=models.PositiveSmallIntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='activity',
            name='activity_type',
            field=models.CharField(choices=[('IND', 'one-on-one lesson'), ('SEM', 'group seminar')], default='SEM', max_length=3),
        ),
    ]
