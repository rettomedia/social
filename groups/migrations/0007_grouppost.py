# Generated by Django 5.1.7 on 2025-03-29 19:06

import autoslug.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0006_alter_member_group'),
        ('network', '0012_regions_customuser_region'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='post_images/')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='message', unique=True)),
                ('writed_at', models.DateTimeField(auto_now_add=True)),
                ('edited_at', models.DateTimeField(auto_now=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='network.regions')),
            ],
            options={
                'verbose_name': 'Group Post',
                'verbose_name_plural': 'Group Posts',
                'db_table': 'group_post',
            },
        ),
    ]
