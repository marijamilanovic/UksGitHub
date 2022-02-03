# Generated by Django 3.2.9 on 2022-02-03 20:54

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, default='')),
                ('color', colorfield.fields.ColorField(default='#FFFFFFFF', image_field=None, max_length=18, samples=None)),
                ('repository', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.repository')),
            ],
        ),
    ]
