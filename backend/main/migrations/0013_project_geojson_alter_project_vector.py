# Generated by Django 4.2.4 on 2023-11-30 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_vector_file_alter_vector_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='geojson',
            field=models.ManyToManyField(blank=True, to='main.geojsonfile'),
        ),
        migrations.AlterField(
            model_name='project',
            name='vector',
            field=models.ManyToManyField(blank=True, to='main.vector'),
        ),
    ]
