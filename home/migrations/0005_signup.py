# Generated by Django 4.2.1 on 2023-05-30 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_rename_password_login_psw'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=122)),
                ('email', models.CharField(max_length=122)),
                ('psw', models.CharField(max_length=20)),
            ],
        ),
    ]
