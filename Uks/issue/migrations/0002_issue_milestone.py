# Generated by Django 4.0 on 2022-01-26 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('milestone', '0001_initial'),
        ('issue', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='milestone',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='milestone.milestone'),
        ),
    ]
