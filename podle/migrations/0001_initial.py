# Generated by Django 2.2.24 on 2021-06-11 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Dictionary",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("word", models.CharField(max_length=254, unique=True)),
                ("pronunciation", models.CharField(max_length=254)),
            ],
            options={
                "verbose_name_plural": "Dictionaries",
                "ordering": ["word"],
            },
        ),
        migrations.CreateModel(
            name="Newsletter",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uuid", models.UUIDField()),
                ("audio_url", models.URLField(blank=True, max_length=2000, null=True)),
                ("object_id", models.PositiveIntegerField()),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.ContentType",
                    ),
                ),
            ],
            options={
                "unique_together": {("content_type", "object_id")},
            },
        ),
    ]
