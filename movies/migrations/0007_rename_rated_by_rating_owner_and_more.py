# Generated by Django 4.2 on 2023-04-25 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='rated_by',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='reviewed_by',
            new_name='owner',
        ),
    ]