# Generated by Django 3.2.5 on 2022-11-06 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20221105_0417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='post',
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('message', 'Message'), ('post', 'Post'), ('alert', 'Alert')], max_length=20),
        ),
    ]
