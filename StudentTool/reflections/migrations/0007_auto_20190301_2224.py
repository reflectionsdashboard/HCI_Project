# Generated by Django 2.1.7 on 2019-03-01 22:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reflections', '0006_auto_20190301_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reflection',
            name='accuracy',
            field=models.IntegerField(blank=True, default=0, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='reflection',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reflection',
            name='student_id',
            field=models.IntegerField(blank=True),
        ),
    ]
