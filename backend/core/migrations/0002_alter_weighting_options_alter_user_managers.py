# Generated by Django 5.1.4 on 2024-12-29 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_alter_animal_age_at_arrival_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weighting',
            options={'permissions': [('can_view_own_weightings', 'Can view own weightings'), ('can_change_own_weightings', 'Can change own weightings')]},
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
    ]
