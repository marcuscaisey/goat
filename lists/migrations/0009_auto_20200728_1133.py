# Generated by Django 3.0.7 on 2020-07-28 11:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("lists", "0008_list_shared_with"),
    ]

    operations = [
        migrations.AlterField(
            model_name="list",
            name="shared_with",
            field=models.ManyToManyField(related_name="shared_lists", to=settings.AUTH_USER_MODEL),
        ),
    ]