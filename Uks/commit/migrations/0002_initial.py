# Generated by Django 4.0 on 2022-02-02 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('repository', '0001_initial'),
        ('commit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commit',
            name='repository',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.repository'),
        ),
    ]
