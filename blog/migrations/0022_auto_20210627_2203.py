# Generated by Django 2.2.4 on 2021-06-27 16:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_auto_20210627_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagemodel',
            name='midUser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mid_user', to=settings.AUTH_USER_MODEL, verbose_name='midUser'),
        ),
    ]