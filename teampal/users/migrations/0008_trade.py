# Generated by Django 5.0.2 on 2024-04-30 21:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_team_creator'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_name', models.CharField(max_length=255)),
                ('item_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('WTB', 'Want to Buy'), ('WTS', 'Want to Sell')], max_length=3)),
                ('quantity', models.IntegerField()),
                ('expected_price', models.FloatField()),
                ('current_offer', models.FloatField()),
                ('current_quantity', models.IntegerField(default=0)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
