# Generated by Django 4.1.2 on 2022-10-15 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MPTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Item name')),
                ('itemdesc', models.CharField(max_length=255, verbose_name='POS Works Description')),
                ('mptp', models.FloatField(verbose_name='Maximum Price to Patient')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date added')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Last modified')),
            ],
            options={
                'verbose_name_plural': 'MPTP',
            },
        ),
    ]
