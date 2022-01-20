# Generated by Django 4.0 on 2022-01-20 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pullrequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('Opened', 'Opened'), ('Closed', 'Closed'), ('Merged', 'Merged')], default='Closed', max_length=20)),
                ('created', models.DateField(blank=True, null=True)),
                ('comments', models.ManyToManyField(to='comment.Comment')),
            ],
        ),
    ]
