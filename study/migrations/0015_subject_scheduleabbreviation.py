# Generated by Django 2.0.4 on 2018-10-28 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0014_auto_20181028_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='scheduleAbbreviation',
            field=models.CharField(max_length=16, null=True),
        ),
    ]
