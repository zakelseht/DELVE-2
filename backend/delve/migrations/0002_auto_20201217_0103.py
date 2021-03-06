# Generated by Django 2.2.4 on 2020-12-17 06:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delve', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ML_Result',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('date_run', models.DateTimeField(blank=True, null=True)),
                ('by_user', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'ML_Result',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=120, unique=True)),
            ],
            options={
                'db_table': 'Tag',
            },
        ),
        migrations.CreateModel(
            name='S3_File',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=120, unique=True)),
                ('uri', models.CharField(max_length=120, unique=True)),
                ('ML_Result_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delve.ML_Result')),
            ],
            options={
                'db_table': 'S3_File',
            },
        ),
        migrations.AddField(
            model_name='ml_result',
            name='tags',
            field=models.ManyToManyField(to='delve.Tag'),
        ),
    ]
