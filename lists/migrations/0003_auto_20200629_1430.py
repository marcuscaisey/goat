# Generated by Django 3.0.7 on 2020-06-29 14:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lists", "0002_auto_20200625_1608"),
    ]

    operations = [
        migrations.CreateModel(
            name="List",
            fields=[("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"))],
        ),
        migrations.AddField(
            model_name="item",
            name="list",
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to="lists.List"),
        ),
    ]