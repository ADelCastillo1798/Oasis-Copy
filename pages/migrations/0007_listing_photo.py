# Generated by Django 3.1.7 on 2021-05-12 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='photo',
        ),
    ]