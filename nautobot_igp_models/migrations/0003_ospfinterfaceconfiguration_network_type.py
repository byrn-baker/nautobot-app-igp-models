# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nautobot_igp_models", "0002_isisconfiguration_default_hello_interval_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="isisinterfaceconfiguration",
            name="network_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("point-to-point", "Point-to-Point"),
                    ("point-to-multipoint", "Point-to-Multipoint"),
                ],
                default="",
                help_text="ISIS network type for this interface.",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="ospfinterfaceconfiguration",
            name="network_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("broadcast", "Broadcast"),
                    ("point-to-point", "Point-to-Point"),
                    ("point-to-multipoint", "Point-to-Multipoint"),
                    ("non-broadcast", "Non-Broadcast (NBMA)"),
                ],
                default="",
                help_text="OSPF network type for this interface.",
                max_length=20,
            ),
        ),
    ]
