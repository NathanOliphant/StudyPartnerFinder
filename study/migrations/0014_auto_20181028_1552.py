# Generated by Django 2.0.4 on 2018-10-28 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0013_auto_20181028_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='year',
            field=models.IntegerField(choices=[(2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025)], default=2018),
        ),
    ]
