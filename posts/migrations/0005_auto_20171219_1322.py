# Generated by Django 2.0 on 2017-12-19 05:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0004_auto_20171218_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to=posts.models.upload_location, width_field='width_field'),
        ),
    ]