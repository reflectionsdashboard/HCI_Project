# Generated by Django 2.1.7 on 2019-02-27 03:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reflections', '0003_auto_20190227_0303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reflection',
            name='inaccuracy_category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='reflections.InAccuracyCategory'),
        ),
        migrations.AlterField(
            model_name='reflection',
            name='topic',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='reflections.Topic'),
        ),
    ]