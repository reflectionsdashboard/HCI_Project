# Generated by Django 2.1.7 on 2019-03-01 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reflections', '0005_auto_20190301_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reflection',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
    ]