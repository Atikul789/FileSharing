# Generated by Django 4.0.5 on 2022-06-06 08:33

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='')),
                ('filehash', models.CharField(max_length=100)),
                ('status', models.BooleanField()),
                ('isRequested', models.BooleanField()),
                ('remark', models.CharField(max_length=20)),
                ('url', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
