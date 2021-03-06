# Generated by Django 4.0 on 2022-02-04 00:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repository', '0001_initial'),
        ('branch', '0002_initial'),
        ('project', '0002_initial'),
        ('pullrequest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pullrequest',
            name='prRepository',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.repository'),
        ),
        migrations.AddField(
            model_name='pullrequest',
            name='projects',
            field=models.ManyToManyField(to='project.Project'),
        ),
        migrations.AddField(
            model_name='pullrequest',
            name='reviewers',
            field=models.ManyToManyField(related_name='pullrequest_reviewers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pullrequest',
            name='source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='source_branch', to='branch.branch'),
        ),
        migrations.AddField(
            model_name='pullrequest',
            name='target',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target_branch', to='branch.branch'),
        ),
    ]
