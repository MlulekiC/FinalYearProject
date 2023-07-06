# Generated by Django 3.2.5 on 2022-11-05 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_notification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-created_on']},
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='date',
            new_name='created_on',
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='user_has_seen',
            new_name='is_read',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='comment',
        ),
        migrations.AddField(
            model_name='notification',
            name='extra_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('message', 'Message'), ('post', 'Post')], max_length=20),
        ),
    ]
