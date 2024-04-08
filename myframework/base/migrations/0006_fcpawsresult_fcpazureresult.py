# Generated by Django 5.0.1 on 2024-02-02 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_sccawsresult_sccazureresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='FcpAwsResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cycleid', models.CharField(max_length=10)),
                ('pass_amt', models.CharField(max_length=50)),
                ('fail_amt', models.CharField(max_length=400)),
                ('create', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FcpAzureResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cycleid', models.CharField(max_length=10)),
                ('pass_amt', models.CharField(max_length=50)),
                ('fail_amt', models.CharField(max_length=400)),
                ('create', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
