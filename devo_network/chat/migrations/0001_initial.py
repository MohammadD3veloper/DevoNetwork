# Generated by Django 4.1.7 on 2023-03-24 01:03

import devo_network.chat.models
import devo_network.utils.randoms
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_prometheus.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Groups",
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
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=100)),
                (
                    "address",
                    models.CharField(
                        default=devo_network.utils.randoms.generate_group_address,
                        max_length=200,
                        unique=True,
                    ),
                ),
                ("about", models.CharField(max_length=200)),
                (
                    "image",
                    models.ImageField(
                        null=True,
                        upload_to=devo_network.chat.models.Groups.group_image_upload_path,
                    ),
                ),
                (
                    "admin",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="admin_on",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "members",
                    models.ManyToManyField(
                        blank=True,
                        related_name="joined_groups",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                django_prometheus.models.ExportModelOperationsMixin("Groups"),
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="Messages",
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
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("message", models.TextField(max_length=800)),
                ("read", models.BooleanField(default=False)),
                ("is_updated", models.BooleanField(default=False)),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to="chat.groups",
                    ),
                ),
                (
                    "reciever",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recived_messages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "reply",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replied_to",
                        to="chat.messages",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                django_prometheus.models.ExportModelOperationsMixin("Messages"),
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="Voices",
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
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                (
                    "voice",
                    models.FileField(
                        upload_to=devo_network.chat.models.Voices.upload_voice_path
                    ),
                ),
                (
                    "message",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="voices",
                        to="chat.messages",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                django_prometheus.models.ExportModelOperationsMixin("Image"),
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="Notification",
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
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("content", models.CharField(max_length=200)),
                (
                    "message",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="chat.messages"
                    ),
                ),
                (
                    "reciever",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recived_notifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_notifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                django_prometheus.models.ExportModelOperationsMixin("Notifications"),
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="Images",
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
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                (
                    "image",
                    models.ImageField(
                        upload_to=devo_network.chat.models.Images.upload_image_path
                    ),
                ),
                (
                    "message",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="chat.messages",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                django_prometheus.models.ExportModelOperationsMixin("Image"),
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="Emojis",
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
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("emoji_name", models.CharField(max_length=100)),
                (
                    "message",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="emojis",
                        to="chat.messages",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                django_prometheus.models.ExportModelOperationsMixin("Emojis"),
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="Documents",
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
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                (
                    "document",
                    models.FileField(
                        upload_to=devo_network.chat.models.Documents.upload_document_path
                    ),
                ),
                (
                    "message",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documents",
                        to="chat.messages",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                django_prometheus.models.ExportModelOperationsMixin("Document"),
                models.Model,
            ),
        ),
    ]
