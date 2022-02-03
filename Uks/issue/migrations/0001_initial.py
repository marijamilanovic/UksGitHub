# Generated by Django 3.2.9 on 2022-02-03 20:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
        ('pullrequest', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('milestone', '0001_initial'),
        ('label', '0001_initial'),
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_title', models.CharField(default='', max_length=50)),
                ('description', models.CharField(default='', max_length=50)),
                ('state', models.CharField(choices=[('Opened', 'Opened'), ('Close', 'Close')], default='Opened', max_length=20)),
                ('opened_by', models.CharField(default='', max_length=50)),
                ('created', models.DateField(blank=True, null=True)),
                ('assignees', models.ManyToManyField(related_name='user_assignees', to=settings.AUTH_USER_MODEL)),
                ('labels', models.ManyToManyField(to='label.Label')),
                ('milestone', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='milestone.milestone')),
                ('projects', models.ManyToManyField(to='project.Project')),
                ('pullrequests', models.ManyToManyField(to='pullrequest.Pullrequest')),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.repository')),
            ],
        ),
    ]
