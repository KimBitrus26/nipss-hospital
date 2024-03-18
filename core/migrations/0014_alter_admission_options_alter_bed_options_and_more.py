# Generated by Django 4.2.9 on 2024-03-16 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_childprescriptionform_is_paid_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admission',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='bed',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='birthreport',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='bloodbankreport',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='bookappointment',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='cabin',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='childcontinuationsheet',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='childprescriptionform',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='children',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='childtestrequestsheet',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='deathreport',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='labtestresult',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='medicine',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='operation',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='patientdiagnostic',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='prescription',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='principalcontinuationsheet',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='principalpatientprescriptionform',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='principalpatienttestrequestsheet',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='spouse',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='spousecontinuationsheet',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='spouseprescriptionform',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='spousetestrequestsheet',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='ward',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AddField(
            model_name='childprescriptionform',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='childprescriptionform',
            name='drugs_dispensed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='principalpatientprescriptionform',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='principalpatientprescriptionform',
            name='drugs_dispensed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='spouseprescriptionform',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='spouseprescriptionform',
            name='drugs_dispensed',
            field=models.BooleanField(default=False),
        ),
    ]