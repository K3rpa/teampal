# Generated by Django 5.0.2 on 2024-05-07 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_tournamentinterest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apex_Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('game', models.CharField(max_length=100)),
                ('members_needed', models.IntegerField()),
                ('contact', models.CharField(max_length=100)),
                ('creator', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
