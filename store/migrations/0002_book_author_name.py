# Generated by Django 4.1.3 on 2022-11-19 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="author_name",
            field=models.CharField(default="author", max_length=255),
            preserve_default=False,
        ),
    ]