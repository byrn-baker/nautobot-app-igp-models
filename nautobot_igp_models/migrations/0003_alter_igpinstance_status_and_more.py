# Generated by Django 4.2.19 on 2025-02-28 21:40

from django.db import migrations
import django.db.models.deletion
import nautobot.extras.models.statuses


class Migration(migrations.Migration):

    dependencies = [
        ('extras', '0114_computedfield_grouping'),
        ('nautobot_igp_models', '0002_remove_ospfconfiguration_area_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='igpinstance',
            name='status',
            field=nautobot.extras.models.statuses.StatusField(null=True, on_delete=django.db.models.deletion.PROTECT, to='extras.status'),
        ),
        migrations.AlterField(
            model_name='isisconfiguration',
            name='status',
            field=nautobot.extras.models.statuses.StatusField(null=True, on_delete=django.db.models.deletion.PROTECT, to='extras.status'),
        ),
        migrations.AlterField(
            model_name='isisinterfaceconfiguration',
            name='status',
            field=nautobot.extras.models.statuses.StatusField(null=True, on_delete=django.db.models.deletion.PROTECT, to='extras.status'),
        ),
        migrations.AlterField(
            model_name='ospfconfiguration',
            name='status',
            field=nautobot.extras.models.statuses.StatusField(null=True, on_delete=django.db.models.deletion.PROTECT, to='extras.status'),
        ),
        migrations.AlterField(
            model_name='ospfinterfaceconfiguration',
            name='status',
            field=nautobot.extras.models.statuses.StatusField(null=True, on_delete=django.db.models.deletion.PROTECT, to='extras.status'),
        ),
    ]
