# Generated by Django 4.0 on 2022-02-03 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('label', '0001_initial'),
        ('issue', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='labels',
            field=models.ManyToManyField(to='label.Label'),
        ),
    ]
