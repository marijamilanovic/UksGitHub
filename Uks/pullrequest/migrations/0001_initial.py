# Generated by Django 3.2.9 on 2022-01-19 23:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('repository', '0001_initial'),
        ('comment', '0001_initial'),
        ('branch', '0001_initial'),
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
                ('prRepository', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.repository')),
                ('source', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='source_branch', to='branch.branch')),
                ('target', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target_branch', to='branch.branch')),
            ],
        ),
    ]
