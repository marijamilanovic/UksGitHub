# Generated by Django 4.0 on 2022-01-29 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('issue', '0005_initial'),
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='repository',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.repository'),
        ),
    ]
