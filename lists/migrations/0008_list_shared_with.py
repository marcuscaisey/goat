# Generated by Django 3.0.7 on 2020-07-27 23:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("lists", "0007_auto_20200726_1931"),
    ]

    operations = [
        migrations.AddField(
            model_name="list", name="shared_with", field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
