# Generated by Django 2.0.4 on 2018-10-28 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0008_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='description',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]