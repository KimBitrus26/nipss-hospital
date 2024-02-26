# Generated by Django 4.2.9 on 2024-02-20 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_patientprincipal_spouse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientprincipal',
            name='spouse',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='spouse_patient', to='core.spouse'),
        ),
    ]
