# Generated by Django 5.0.1 on 2024-01-26 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alltestcase'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestResults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cycleid', models.CharField(max_length=10)),
                ('testcaseid', models.CharField(max_length=50)),
                ('usecase', models.CharField(max_length=400)),
                ('result', models.CharField(max_length=10)),
                ('create', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
