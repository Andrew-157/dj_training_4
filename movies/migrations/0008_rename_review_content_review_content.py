# Generated by Django 4.2 on 2023-04-28 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_rename_rated_by_rating_owner_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='review_content',
            new_name='content',
        ),
    ]
