# Generated by Django 2.2.4 on 2021-06-24 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_chatters'),
    ]

    operations = [
        migrations.AddField(
            model_name='register_table',
            name='max_num',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='chatters',
            name='num',
            field=models.BigIntegerField(default=0),
        ),
    ]
