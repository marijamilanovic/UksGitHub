# Generated by Django 4.0 on 2022-01-27 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_title', models.CharField(default='', max_length=50)),
                ('state', models.CharField(choices=[('Opened', 'Opened'), ('Close', 'Close')], default='Opened', max_length=20)),
                ('opened_by', models.CharField(default='', max_length=50)),
                ('assignee', models.CharField(default='', max_length=50)),
                ('description', models.CharField(max_length=50)),
            ],
        ),
    ]
