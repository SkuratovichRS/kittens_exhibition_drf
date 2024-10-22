# Generated by Django 5.1.1 on 2024-10-05 14:15

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Kitten',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=50)),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('description', models.CharField(max_length=200)),
                ('breed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kittens', to='exhibition.breed')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kittens', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('kitten', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='exhibition.kitten')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'kitten')},
            },
        ),
    ]
