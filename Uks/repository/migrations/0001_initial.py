# Generated by Django 3.2.9 on 2022-01-29 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('Public', 'Public'), ('Private', 'Private')], default='Private', max_length=20)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_creator', to=settings.AUTH_USER_MODEL)),
                ('developers', models.ManyToManyField(related_name='user_developers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
