# Generated by Django 5.0.2 on 2024-02-29 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_customuser_background_image_customuser_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]