# Generated by Django 4.2.4 on 2023-09-28 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='district',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='projects', to='api.district'),
        ),
        migrations.AlterField(
            model_name='project',
            name='municipality',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='projects', to='api.municipality'),
        ),
        migrations.AlterField(
            model_name='project',
            name='province',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='projects', to='api.province'),
        ),
    ]
