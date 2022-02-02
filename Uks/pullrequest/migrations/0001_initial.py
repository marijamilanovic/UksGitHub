# Generated by Django 4.0 on 2022-02-01 22:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('label', '0001_initial'),
        ('milestone', '0002_initial'),
        ('comment', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pullrequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('Opened', 'Opened'), ('Closed', 'Closed'), ('Merged', 'Merged')], default='Opened', max_length=20)),
                ('created', models.DateField(blank=True, null=True)),
                ('reviewed', models.BooleanField(default=False)),
                ('assignees', models.ManyToManyField(related_name='pullrequest_assignees', to=settings.AUTH_USER_MODEL)),
                ('comments', models.ManyToManyField(to='comment.Comment')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
                ('labels', models.ManyToManyField(to='label.Label')),
                ('milestone', models.ManyToManyField(to='milestone.Milestone')),
            ],
        ),
    ]
