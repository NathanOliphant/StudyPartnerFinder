# Generated by Django 2.0.4 on 2018-11-07 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0020_studygroup_posttitle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studygroup',
            name='weekday',
        ),
        migrations.RemoveField(
            model_name='studygroup',
            name='weekend',
        ),
        migrations.AddField(
            model_name='studygroup',
            name='daysAvailable',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='studygroup',
            name='genderSpecific',
            field=models.CharField(choices=[('U', 'Undeclared'), ('M', 'Male'), ('F', 'Female'), ('N', 'Nonbinary')], max_length=15),
        ),
    ]
