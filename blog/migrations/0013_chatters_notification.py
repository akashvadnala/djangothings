# Generated by Django 2.2.4 on 2021-06-25 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20210624_2335'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatters',
            name='notification',
            field=models.BooleanField(default=False),
        ),
    ]
