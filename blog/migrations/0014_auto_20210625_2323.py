# Generated by Django 2.2.4 on 2021-06-25 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_chatters_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register_table',
            name='max_num',
            field=models.BigIntegerField(default=2),
        ),
    ]
