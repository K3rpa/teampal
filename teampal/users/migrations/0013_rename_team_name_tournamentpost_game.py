# Generated by Django 5.0.2 on 2024-05-06 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_tournamentpost_team_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tournamentpost',
            old_name='team_name',
            new_name='game',
        ),
    ]
