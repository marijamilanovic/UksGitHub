# Generated by Django 4.0 on 2022-01-29 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('issue', '0004_initial'),
        ('pullrequest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='pullrequests',
            field=models.ManyToManyField(to='pullrequest.Pullrequest'),
        ),
    ]