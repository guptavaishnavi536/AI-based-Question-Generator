# Generated by Django 4.2.1 on 2023-06-27 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_remove_qna_sub_name_alter_qna_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qna',
            name='pdf',
            field=models.FileField(null=True, upload_to='pdf/'),
        ),
    ]
