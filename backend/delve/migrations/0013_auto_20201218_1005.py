# Generated by Django 2.2.4 on 2020-12-18 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delve', '0012_auto_20201218_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ml_result',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='s3_file',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tag',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]
