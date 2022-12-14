# Generated by Django 4.0.5 on 2022-06-11 18:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('filesharing', '0009_file_mimetype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='isRequested',
            new_name='blocking_status',
        ),
        migrations.RenameField(
            model_name='file',
            old_name='status',
            new_name='request_accept',
        ),
        migrations.RemoveField(
            model_name='file',
            name='mimetype',
        ),
        migrations.RemoveField(
            model_name='file',
            name='remark',
        ),
        migrations.AddField(
            model_name='file',
            name='unblocking_information',
            field=models.CharField(blank=True, max_length=2000),
        ),
    ]
