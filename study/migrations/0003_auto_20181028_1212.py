# Generated by Django 2.0.4 on 2018-10-28 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0002_auto_20181028_1151'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StudyGroup_Filter',
            new_name='StudyGroupFilter',
        ),
        migrations.RenameField(
            model_name='studygroup',
            old_name='active',
            new_name='isActive',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='acceptedTOS',
            new_name='hasAcceptedTOS',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='active',
            new_name='isActive',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='adminUser',
            new_name='isAdminUser',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='verified',
            new_name='isVerified',
        ),
    ]