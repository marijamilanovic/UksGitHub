# Generated by Django 3.2.9 on 2022-01-19 23:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pullrequest', '0001_initial'),
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='task.task')),
                ('issue_title', models.CharField(max_length=50)),
                ('state', models.CharField(choices=[('Opened', 'Opened'), ('Close', 'Close')], default='Opened', max_length=20)),
                ('pullrequests', models.ManyToManyField(to='pullrequest.Pullrequest')),
            ],
            bases=('task.task',),
        ),
    ]
