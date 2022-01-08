# Generated by Django 4.0 on 2022-01-04 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creator', to='auth.user'),
        ),
        migrations.AlterField(
            model_name='repository',
            name='developers',
            field=models.ManyToManyField(related_name='user_developers', to=settings.AUTH_USER_MODEL),
        ),
    ]