# Generated by Django 4.1.7 on 2023-03-02 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("borrowing", "0003_alter_borrow_actual_return_alter_borrow_borrow_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="borrow",
            name="status",
            field=models.BooleanField(default=False),
        ),
    ]
