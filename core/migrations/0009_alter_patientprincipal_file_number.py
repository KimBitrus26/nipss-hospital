# Generated by Django 4.2.9 on 2024-02-21 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_children_file_number_alter_children_last_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientprincipal',
            name='file_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]