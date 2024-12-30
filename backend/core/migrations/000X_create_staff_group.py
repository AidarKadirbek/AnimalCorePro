from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_weighting_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inventory_number', models.CharField(max_length=100, unique=True, verbose_name='Инвентарный номер')),
                ('gender', models.CharField(max_length=10, verbose_name='Пол')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('arrival_date', models.DateField(verbose_name='Дата поступления')),
                ('age_at_arrival', models.IntegerField(verbose_name='Возраст на момент поступления (в месяцах)')),
                ('breed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Breed', verbose_name='Порода')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Animal', verbose_name='Родитель')),
            ],
        ),
        migrations.CreateModel(
            name='Weighting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата взвешивания')),
                ('weight', models.FloatField(default=0.0, verbose_name='Вес')),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Animal', verbose_name='Животное')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'unique_together': {('animal', 'date')},
            },
        ),
    ]