# Generated by Django 4.1.7 on 2023-03-11 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="userProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "profile_picture",
                    models.ImageField(
                        blank=True, null=True, upload_to="user/profile_pictures"
                    ),
                ),
                (
                    "cover_photo",
                    models.ImageField(
                        blank=True, null=True, upload_to="user/cover_photos"
                    ),
                ),
                (
                    "address_line_1",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "address_line_2",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("country", models.CharField(blank=True, max_length=25, null=True)),
                ("district", models.CharField(blank=True, max_length=25, null=True)),
                ("concelho", models.CharField(blank=True, max_length=25, null=True)),
                (
                    "codigo_postal",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                ("latitude", models.CharField(blank=True, max_length=25, null=True)),
                ("longitude", models.CharField(blank=True, max_length=25, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
