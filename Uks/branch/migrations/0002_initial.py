# Generated by Django 4.0 on 2022-02-02 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('repository', '0001_initial'),
        ('branch', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='repository',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.repository'),
        ),
    ]
