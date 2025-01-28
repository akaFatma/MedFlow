# Generated by Django 5.1.4 on 2024-12-25 19:02

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bilan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prescription', models.CharField(help_text='Description de la prescription pour cet examen', max_length=255)),
                ('date_emission', models.DateField(auto_now_add=True, verbose_name="Date d'émission")),
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
            name='Medecin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('specialite', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ordonnance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_emission', models.DateField(auto_now_add=True, verbose_name="Date d'émission")),
                ('status', models.CharField(choices=[('distribuee', 'Distribuée'), ('en_attente', 'En attente'), ('validee', 'Validée')], default='en_attente', help_text="Statut actuel de l'ordonnance", max_length=100)),
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
            name='test',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Traitement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('dose', models.CharField(max_length=100)),
                ('consommation', models.CharField(help_text="Par exemple : '3 comprimés'", max_length=100)),
                ('frequence', models.IntegerField(help_text='Par exemple : tous les 3 jours', verbose_name='Fréquence (en jours)')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('patient', 'Patient'), ('medecin', 'Médecin'), ('admin', 'Admin')], default='Patient', max_length=30)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BilanBiologique',
            fields=[
                ('bilan_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='med.bilan')),
                ('resultat', models.TextField(help_text='Résultat du bilan biologique')),
            ],
            bases=('med.bilan',),
        ),
        migrations.CreateModel(
            name='BilanRadiologique',
            fields=[
                ('bilan_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='med.bilan')),
                ('compte_rendu', models.TextField(help_text='Compte-rendu du bilan radiologique')),
                ('image_url', models.URLField(blank=True, help_text="Lien vers l'image radiologique (optionnel)", null=True)),
            ],
            bases=('med.bilan',),
        ),
        migrations.AddField(
            model_name='bilan',
            name='consultation',
            field=models.ForeignKey(help_text='Consultation à laquelle ce bilan est associé', on_delete=django.db.models.deletion.CASCADE, related_name='bilans', to='med.consultation'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='dpi',
            field=models.ForeignKey(blank=True, default=None, help_text='DPI associé à cette consultation', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consultations', to='med.dpi'),
        ),
        migrations.AddField(
            model_name='consultation',
            name='ordonnance',
            field=models.ForeignKey(blank=True, help_text='Ordonnance liée à cette consultation (optionnelle)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consultations', to='med.ordonnance'),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('date_de_naissance', models.CharField(max_length=100)),
                ('adresse', models.TextField()),
                ('telephone', models.CharField(max_length=15)),
                ('nss', models.CharField(max_length=15, unique=True)),
                ('mutuelle', models.CharField(blank=True, max_length=100, null=True)),
                ('medecins', models.ManyToManyField(blank=True, related_name='patients', to='med.medecin')),
                ('personne_a_contacter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patients', to='med.personneacontacter')),
            ],
        ),
        migrations.AddField(
            model_name='ordonnance',
            name='patient',
            field=models.ForeignKey(help_text='Patient associé à cette ordonnance', on_delete=django.db.models.deletion.CASCADE, related_name='ordonnances', to='med.patient'),
        ),
        migrations.AddField(
            model_name='dpi',
            name='patient',
            field=models.OneToOneField(help_text='Le patient associé à ce DSI', on_delete=django.db.models.deletion.CASCADE, related_name='dossier_patient', to='med.patient'),
        ),
        migrations.AddField(
            model_name='ordonnance',
            name='traitements',
            field=models.ManyToManyField(help_text='Liste des traitements inclus dans cette ordonnance', related_name='ordonnances', to='med.traitement'),
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=30)),
                ('telephone', models.CharField(max_length=15)),
                ('etablissement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='utilisateurs', to='med.etablissement')),
            ],
        ),
        migrations.AddField(
            model_name='dpi',
            name='utilisateur',
            field=models.OneToOneField(help_text="L'utilisateur associé à ce DSI", on_delete=django.db.models.deletion.CASCADE, related_name='dossier_utilisateur', to='med.utilisateur'),
        ),
    ]
