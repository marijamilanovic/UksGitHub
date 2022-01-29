# Generated by Django 4.0 on 2022-01-29 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pullrequest', '0001_initial'),
        ('branch', '0002_initial'),
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pullrequest',
            name='prRepository',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.repository'),
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
