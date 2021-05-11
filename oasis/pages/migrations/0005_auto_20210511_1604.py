# Generated by Django 3.1.7 on 2021-05-11 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_merge_20210511_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='state',
            field=models.CharField(blank=True, choices=[('0', 'In Progress'), ('1', 'Pending - buyer marked complete'), ('2', 'Pending - seller marked complete'), ('3', 'Completed')], default=0, help_text='Conversation status', max_length=1),
        ),
    ]