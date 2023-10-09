# Generated by Django 3.2.21 on 2023-10-09 09:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0006_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='shared_with',
            field=models.ManyToManyField(blank=True, related_name='shared_folders', to=settings.AUTH_USER_MODEL),
        ),
    ]
