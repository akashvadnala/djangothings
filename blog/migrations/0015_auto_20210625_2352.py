# Generated by Django 2.2.4 on 2021-06-25 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20210625_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatters',
            name='last_msg',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chatters',
            name='last_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
