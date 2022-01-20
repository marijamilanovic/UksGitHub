# Generated by Django 3.2.9 on 2022-01-19 23:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('description', models.TextField(blank=True, default='')),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.repository')),
            ],
        ),
    ]
