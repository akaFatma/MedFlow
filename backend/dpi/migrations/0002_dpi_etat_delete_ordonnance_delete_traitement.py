# Generated by Django 5.1.4 on 2024-12-26 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dpi',
            name='etat',
            field=models.CharField(choices=[('ouvert', 'ouvert'), ('fermé', 'fermé')], default='ouvert', max_length=10),
        ),
        migrations.DeleteModel(
            name='Ordonnance',
        ),
        migrations.DeleteModel(
            name='Traitement',
        ),
    ]
