# Generated by Django 4.0 on 2022-01-31 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, default='')),
                ('created_date', models.DateTimeField(blank=True, null=True)),
                ('changed_object_id', models.IntegerField()),
                ('object_type', models.CharField(choices=[('Milestone', 'Milestone'), ('Issue', 'Issue'), ('Project', 'Project'), ('Pull request', 'Pull request'), ('Label', 'Label'), ('Assignees', 'Assignees'), ('Changes', 'Changes'), ('Comments', 'Comments'), ('Approved', 'Approved')], default='Changes', max_length=20)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
