# Generated by Django 3.2.16 on 2023-02-06 21:45

from django.db import migrations, models

import polytrip.siteconfig.models


class Migration(migrations.Migration):
    dependencies = [
        ("siteconfig", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteconfiguration",
            name="end_date",
            field=models.DateTimeField(
                default=polytrip.siteconfig.models.get_default_end_date,
                help_text="End date of the Polytrip event",
                verbose_name="End date",
            ),
        ),
    ]