# Generated by Django 5.0.2 on 2024-05-06 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_tournamentpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentpost',
            name='team_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
