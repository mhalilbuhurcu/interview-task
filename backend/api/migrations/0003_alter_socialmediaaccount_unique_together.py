# Generated by Django 5.1.6 on 2025-02-20 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_influencer_content_type_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='socialmediaaccount',
            unique_together={('platform', 'username')},
        ),
    ]
