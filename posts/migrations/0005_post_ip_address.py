# Generated by Django 5.1.7 on 2025-03-24 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_comment_post_alter_like_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]
