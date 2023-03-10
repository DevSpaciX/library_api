# Generated by Django 4.1.7 on 2023-03-07 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('author', models.CharField(max_length=128)),
                ('cover', models.BooleanField(choices=[(0, 'Hard'), (1, 'Soft')])),
                ('inventory', models.PositiveIntegerField()),
                ('daily_fee', models.DecimalField(decimal_places=2, max_digits=5)),
                ('need_to_refill', models.BooleanField(default=False)),
            ],
        ),
    ]
