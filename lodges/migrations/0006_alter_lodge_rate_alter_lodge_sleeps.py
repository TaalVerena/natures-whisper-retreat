# Generated by Django 4.2.11 on 2024-08-05 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lodges", "0005_alter_lodge_amenityimage1_alter_lodge_amenityimage2"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lodge",
            name="rate",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name="lodge",
            name="sleeps",
            field=models.IntegerField(),
        ),
    ]
