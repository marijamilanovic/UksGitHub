# Generated by Django 4.0 on 2022-01-19 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=50)),
                ('description', models.TextField(blank=True, default='')),
                ('status', models.CharField(choices=[('Opened', 'Opened'), ('Closed', 'Closed')], default='Opened', max_length=20)),
                ('created', models.DateField(auto_now_add=True)),
                ('due_date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
