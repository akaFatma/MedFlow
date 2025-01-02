# Generated by Django 5.1.4 on 2025-01-02 19:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Examen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prescription', models.CharField(help_text='Description de la prescription pour cet examen', max_length=255)),
                ('date_emission', models.DateField(verbose_name="Date d'émission")),
            ],
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, help_text='Date à laquelle la consultation a eu lieu', verbose_name='Date de consultation')),
                ('resume', models.CharField(help_text='Résumé de la consultation', max_length=2500)),
            ],
        ),
        migrations.CreateModel(
            name='DPI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etat', models.CharField(choices=[('ouvert', 'ouvert'), ('fermé', 'fermé')], default='ouvert', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Etablissement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('adresse', models.TextField()),
                ('telephone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Ordonnance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('validee', models.BooleanField(default=False)),
                ('date_emission', models.DateField(auto_now_add=True, verbose_name="Date d'émission")),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('date_de_naissance', models.DateField()),
                ('adresse', models.TextField()),
                ('telephone', models.CharField(max_length=15)),
                ('nss', models.CharField(max_length=15, unique=True)),
                ('mutuelle', models.CharField(blank=True, max_length=100, null=True)),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='qr_codes/')),
            ],
        ),
        migrations.CreateModel(
            name='PersonneAContacter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('telephone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Soin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etat', models.CharField(help_text='État associé', max_length=100)),
                ('medicament', models.CharField(help_text='Nom du médicament', max_length=255)),
                ('autre', models.TextField(blank=True, help_text='Autre information supplémentaire', null=True)),
                ('date', models.DateField(help_text='Date de création du soin')),
            ],
        ),
        migrations.CreateModel(
            name='Traitement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('dose', models.CharField(max_length=100)),
                ('consommation', models.CharField(help_text="Par exemple : '3 comprimés'", max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BilanBiologique',
            fields=[
                ('examen_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='med.examen')),
                ('resultat', models.TextField(help_text='Résultat du bilan biologique')),
            ],
            bases=('med.examen',),
        ),
        migrations.CreateModel(
            name='BilanRadiologique',
            fields=[
                ('examen_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='med.examen')),
                ('compte_rendu', models.TextField(help_text='Compte-rendu du bilan radiologique')),
                ('image_url', models.ImageField(blank=True, null=True, upload_to='radio/')),
            ],
            bases=('med.examen',),
        ),
        migrations.AddField(
            model_name='examen',
            name='consultation',
            field=models.ForeignKey(help_text='Consultation à laquelle cet examen est associé', on_delete=django.db.models.deletion.CASCADE, related_name='examens_from_examen', to='med.consultation'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='examens',
            field=models.ManyToManyField(blank=True, help_text='Examens associés à cette consultation', related_name='consultations_from_examens', to='med.examen'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='dpi',
            field=models.ForeignKey(blank=True, default=None, help_text='DPI associé à cette consultation', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consultations', to='med.dpi'),
        ),
        migrations.CreateModel(
            name='Medecin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialite', models.CharField(max_length=100)),
                ('etablissement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='medecins', to='med.etablissement')),
            ],
        ),
    ]
