# Generated by Django 4.1.2 on 2022-10-15 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppxl', '0003_mptp_mptp_applies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mptp',
            name='mptp',
            field=models.FloatField(blank=True, verbose_name='Maximum Price to Patient'),
        ),
    ]