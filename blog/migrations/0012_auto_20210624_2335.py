# Generated by Django 2.2.4 on 2021-06-24 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20210624_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register_table',
            name='max_num',
            field=models.BigIntegerField(default=1),
        ),
    ]