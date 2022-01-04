# Generated by Django 4.0 on 2022-01-04 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('comment', '0002_alter_comment_author'),
        ('task', '0002_alter_task_assigned_alter_task_author'),
        ('commit', '0002_alter_commit_author'),
        ('repository', '0002_alter_repository_creator_alter_repository_developers'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Administrator', 'Administrator'), ('Authenticate user', 'Authenticate user'), ('Unauthenticate user', 'Unauthenticate user')], default='Unauthenticate user', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
