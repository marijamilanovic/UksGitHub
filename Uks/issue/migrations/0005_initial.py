# Generated by Django 4.0 on 2022-02-02 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pullrequest', '0001_initial'),
        ('issue', '0004_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='pullrequests',
            field=models.ManyToManyField(to='pullrequest.Pullrequest'),
        ),
    ]