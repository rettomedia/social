# Generated by Django 5.0.2 on 2024-02-17 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_news'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': 'New', 'verbose_name_plural': 'News'},
        ),
    ]