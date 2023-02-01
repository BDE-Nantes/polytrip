# Generated by Django 3.2.16 on 2023-01-27 18:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("schools", "0001_initial"),
        ("accounts", "0003_user_school"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="school",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to="schools.school", verbose_name="School"
            ),
        ),
    ]
