# Generated by Django 4.2.11 on 2024-08-11 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contact", "0003_contactrequest_lodge_reply_contactrequest_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contactrequest",
            name="status",
            field=models.CharField(default="pending", max_length=50),
        ),
    ]