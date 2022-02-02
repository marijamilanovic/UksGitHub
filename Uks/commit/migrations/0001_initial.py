# Generated by Django 4.0 on 2022-02-02 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('branch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, default='')),
                ('date_time', models.DateTimeField()),
                ('hash_id', models.CharField(max_length=100)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branch.branch')),
            ],
        ),
    ]
