# Generated by Django 4.2 on 2025-02-06 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0010_alter_categories_options_alter_hairlength_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="masters",
            name="discount",
            field=models.DecimalField(
                decimal_places=2, default=0.0, max_digits=5, verbose_name="Скидка в %"
            ),
        ),
    ]
