# Generated by Django 4.2 on 2025-02-06 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "services",
            "0002_alter_price_unique_together_remove_price_hair_length_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="products",
            name="master",
        ),
        migrations.AddField(
            model_name="products",
            name="master",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="products",
                to="services.masters",
                verbose_name="Мастер",
            ),
        ),
    ]
