# Generated by Django 4.2.9 on 2024-02-20 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_patientprincipal_file_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientprincipal',
            name='file_number',
            field=models.CharField(editable=False, max_length=10),
        ),
    ]
