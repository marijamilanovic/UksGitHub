# Generated by Django 4.0 on 2022-01-20 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
        ('milestone', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.project'),
        ),
    ]
