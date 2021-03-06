# Generated by Django 4.0 on 2022-02-04 00:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('Public', 'Public'), ('Private', 'Private')], default='Private', max_length=20)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creator', to='auth.user')),
                ('developers', models.ManyToManyField(related_name='user_developers', to=settings.AUTH_USER_MODEL)),
                ('forks', models.ManyToManyField(related_name='user_forks', to=settings.AUTH_USER_MODEL)),
                ('stargazers', models.ManyToManyField(related_name='user_stargazers', to=settings.AUTH_USER_MODEL)),
                ('watchers', models.ManyToManyField(related_name='user_watchers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
