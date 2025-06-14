# Generated by Django 5.1.3 on 2025-01-23 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tresorerie', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caisse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type_caisse', models.CharField(max_length=50, verbose_name='Type de Caisse')),
                ('type', models.CharField(max_length=50, verbose_name="Type d'opération")),
                ('date', models.DateField(verbose_name="Date de l'opération")),
                ('motif', models.TextField(verbose_name='Motif')),
                ('somme', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Somme')),
                ('total_grande_caisse', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Total Grande Caisse')),
                ('total_petite_caisse', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Total Petite Caisse')),
            ],
        ),
    ]
