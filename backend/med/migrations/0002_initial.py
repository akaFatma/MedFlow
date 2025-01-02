# Generated by Django 5.1.4 on 2025-01-02 19:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('med', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='medecin',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ordonnance',
            name='dpi',
            field=models.ForeignKey(help_text='DPI associé à cette ordonnance', on_delete=django.db.models.deletion.CASCADE, related_name='dpi', to='med.dpi'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='ordonnance',
            field=models.ForeignKey(blank=True, help_text='Ordonnance liée à cette consultation (optionnelle)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consultations', to='med.ordonnance'),
        ),
        migrations.AddField(
            model_name='patient',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dpi',
            name='patient',
            field=models.OneToOneField(help_text='Le patient associé à ce DSI', on_delete=django.db.models.deletion.CASCADE, related_name='dossier_patient', to='med.patient'),
        ),
        migrations.AddField(
            model_name='patient',
            name='personne_a_contacter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patients', to='med.personneacontacter'),
        ),
        migrations.AddField(
            model_name='soin',
            name='dpi',
            field=models.ForeignKey(help_text='DPI auquel ce soin est associé', on_delete=django.db.models.deletion.CASCADE, related_name='soins', to='med.dpi'),
        ),
        migrations.AddField(
            model_name='ordonnance',
            name='traitements',
            field=models.ManyToManyField(help_text='Liste des traitements inclus dans cette ordonnance', related_name='ordonnances', to='med.traitement'),
        ),
    ]
