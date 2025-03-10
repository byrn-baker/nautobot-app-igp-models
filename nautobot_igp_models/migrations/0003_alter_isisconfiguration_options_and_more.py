# Generated by Django 4.2.19 on 2025-03-02 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nautobot_igp_models', '0002_alter_igproutinginstance_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='isisconfiguration',
            options={},
        ),
        migrations.AlterField(
            model_name='isisconfiguration',
            name='instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nautobot_igp_models.igproutinginstance'),
        ),
        migrations.AlterField(
            model_name='isisconfiguration',
            name='system_id',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name='isisconfiguration',
            unique_together={('instance', 'name')},
        ),
    ]
