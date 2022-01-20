# Generated by Django 4.0 on 2022-01-20 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('milestone', '0003_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_title', models.CharField(default=' ', max_length=50)),
                ('opened', models.DateField(auto_now_add=True)),
                ('closed', models.DateField(blank=True, null=True)),
                ('assigned', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to='auth.user')),
                ('milestone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='milestone.milestone')),
            ],
        ),
    ]
