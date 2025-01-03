# Generated by Django 4.2.9 on 2024-02-20 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_patientprincipal_file_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientprincipal',
            name='spouse',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='spouse_patient', to='core.spouse'),
        ),
    ]
