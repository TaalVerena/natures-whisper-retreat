# Generated by Django 4.2.11 on 2024-08-11 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contact", "0004_alter_contactrequest_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contactrequest",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("in_progress", "In Progress"),
                    ("resolved", "Resolved"),
                ],
                default="pending",
                max_length=12,
            ),
        ),
    ]
