# Generated by Django 4.0 on 2022-02-03 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
        ('issue', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='projects',
            field=models.ManyToManyField(to='project.Project'),
        ),
    ]
