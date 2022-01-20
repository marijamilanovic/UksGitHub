# Generated by Django 4.0 on 2022-01-20 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('repository', '0001_initial'),
        ('issue', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='repository',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.repository'),
        ),
    ]
