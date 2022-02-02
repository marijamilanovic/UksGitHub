# Generated by Django 4.0 on 2022-02-02 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('description', models.TextField(blank=True, default='')),
                ('status', models.CharField(choices=[('Opened', 'Opened'), ('Closed', 'Closed')], default='Opened', max_length=20)),
            ],
        ),
    ]
