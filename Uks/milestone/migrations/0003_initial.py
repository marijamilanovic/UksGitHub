# Generated by Django 4.0 on 2022-02-03 22:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('milestone', '0002_initial'),
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='repository',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.repository'),
        ),
    ]
