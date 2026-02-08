"""Management command to load IGP config context schemas and export templates."""

import json
import os

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from nautobot.extras.models import ConfigContextSchema, ExportTemplate

from nautobot_igp_models.models import ISISConfiguration, OSPFConfiguration


class Command(BaseCommand):
    """Load IGP config context schemas and export templates into Nautobot."""

    help = "Load IGP config context schemas and export templates"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force update existing templates and schemas",
        )

    def handle(self, *args, **options):
        """Execute the command."""
        force = options["force"]

        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("Loading IGP Resources"))
        self.stdout.write("=" * 70 + "\n")

        # Get the base directory for the app
        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

        # Load Config Context Schemas
        self.load_config_context_schemas(base_dir, force)

        # Load Export Templates
        self.load_export_templates(base_dir, force)

        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("✓ IGP resources loaded successfully"))
        self.stdout.write("=" * 70 + "\n")

    def load_config_context_schemas(self, base_dir, force=False):
        """Load config context schemas from JSON files."""
        self.stdout.write("\n" + self.style.SUCCESS("Config Context Schemas:"))
        self.stdout.write("-" * 70)

        schemas_dir = os.path.join(base_dir, "schemas")
        schemas = [
            {
                "name": "IGP ISIS Configuration",
                "description": "JSON Schema for ISIS config context parameters",
                "file": "config_context_isis.json",
            },
            {
                "name": "IGP OSPF Configuration",
                "description": "JSON Schema for OSPF config context parameters",
                "file": "config_context_ospf.json",
            },
        ]

        for schema_def in schemas:
            schema_file = os.path.join(schemas_dir, schema_def["file"])

            if not os.path.exists(schema_file):
                self.stdout.write(
                    self.style.WARNING(f"  ⊘ Schema file not found: {schema_file}")
                )
                continue

            # Load schema content
            with open(schema_file, "r", encoding="utf-8") as f:
                schema_data = json.load(f)

            # Check if schema exists
            existing = ConfigContextSchema.objects.filter(name=schema_def["name"]).first()

            if existing and not force:
                self.stdout.write(
                    self.style.WARNING(
                        f"  ⊘ Schema already exists: {schema_def['name']} (use --force to update)"
                    )
                )
                continue

            # Create or update schema
            schema, created = ConfigContextSchema.objects.update_or_create(
                name=schema_def["name"],
                defaults={
                    "description": schema_def["description"],
                    "data_schema": schema_data,
                },
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"  ✓ Created: {schema_def['name']}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"  ✓ Updated: {schema_def['name']}"))

    def load_export_templates(self, base_dir, force=False):
        """Load export templates from Jinja2 files."""
        self.stdout.write("\n" + self.style.SUCCESS("Export Templates:"))
        self.stdout.write("-" * 70)

        templates_dir = os.path.join(base_dir, "templates", "config_templates")

        # Get content types
        isis_ct = ContentType.objects.get_for_model(ISISConfiguration)
        ospf_ct = ContentType.objects.get_for_model(OSPFConfiguration)

        templates = [
            # Cisco IOS Templates
            {
                "name": "ISIS Configuration (Cisco IOS)",
                "content_type": isis_ct,
                "description": "Generate Cisco IOS ISIS configuration",
                "file": "cisco_ios_isis.j2",
                "template_code": None,  # Will be loaded from file
                "mime_type": "text/plain",
                "file_extension": "txt",
            },
            {
                "name": "OSPF Configuration (Cisco IOS)",
                "content_type": ospf_ct,
                "description": "Generate Cisco IOS OSPF configuration",
                "file": "cisco_ios_ospf.j2",
                "template_code": None,
                "mime_type": "text/plain",
                "file_extension": "txt",
            },
            # Cisco IOS XR Templates
            {
                "name": "ISIS Configuration (Cisco IOS XR)",
                "content_type": isis_ct,
                "description": "Generate Cisco IOS XR ISIS configuration",
                "file": "cisco_iosxr_isis.j2",
                "template_code": None,
                "mime_type": "text/plain",
                "file_extension": "txt",
            },
            {
                "name": "OSPF Configuration (Cisco IOS XR)",
                "content_type": ospf_ct,
                "description": "Generate Cisco IOS XR OSPF configuration",
                "file": "cisco_iosxr_ospf.j2",
                "template_code": None,
                "mime_type": "text/plain",
                "file_extension": "txt",
            },
            # Juniper JunOS Templates
            {
                "name": "ISIS Configuration (Juniper JunOS)",
                "content_type": isis_ct,
                "description": "Generate Juniper JunOS ISIS configuration",
                "file": "juniper_isis.j2",
                "template_code": None,
                "mime_type": "text/plain",
                "file_extension": "txt",
            },
            # Arista EOS Templates
            {
                "name": "ISIS Configuration (Arista EOS)",
                "content_type": isis_ct,
                "description": "Generate Arista EOS ISIS configuration",
                "file": "arista_eos_isis.j2",
                "template_code": None,
                "mime_type": "text/plain",
                "file_extension": "txt",
            },
            {
                "name": "OSPF Configuration (Arista EOS)",
                "content_type": ospf_ct,
                "description": "Generate Arista EOS OSPF configuration",
                "file": "arista_eos_ospf.j2",
                "template_code": None,
                "mime_type": "text/plain",
                "file_extension": "txt",
            },
        ]

        for template_def in templates:
            template_file = os.path.join(templates_dir, template_def["file"])

            if not os.path.exists(template_file):
                self.stdout.write(
                    self.style.WARNING(f"  ⊘ Template file not found: {template_file}")
                )
                continue

            # Load template content
            with open(template_file, "r", encoding="utf-8") as f:
                template_code = f.read()

            # Prepare template for ISIS Configuration
            # Need to wrap it to work with export template context
            if template_def["content_type"] == isis_ct:
                template_code = self._wrap_isis_template(template_code)
            elif template_def["content_type"] == ospf_ct:
                template_code = self._wrap_ospf_template(template_code)

            # Check if template exists
            existing = ExportTemplate.objects.filter(
                content_type=template_def["content_type"],
                name=template_def["name"],
            ).first()

            if existing and not force:
                self.stdout.write(
                    self.style.WARNING(
                        f"  ⊘ Template already exists: {template_def['name']} (use --force to update)"
                    )
                )
                continue

            # Create or update template
            template, created = ExportTemplate.objects.update_or_create(
                content_type=template_def["content_type"],
                name=template_def["name"],
                defaults={
                    "description": template_def["description"],
                    "template_code": template_code,
                    "mime_type": template_def["mime_type"],
                    "file_extension": template_def["file_extension"],
                },
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"  ✓ Created: {template_def['name']}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"  ✓ Updated: {template_def['name']}"))

    def _wrap_isis_template(self, template_code):
        """Wrap ISIS template for export template context."""
        # Export templates can be called from detail page (single object) or list page (queryset)
        # For queryset exports, we need to iterate. For single object, we access directly.
        wrapper = """{# Export Template Wrapper for ISISConfiguration #}
{# Handle both single object and queryset export contexts #}
{% if queryset is defined %}
{# Queryset export - iterate over objects #}
{% for isis_config in queryset %}
{% set interfaces = isis_config.interface_configurations.all %}
{% set device_config_context = isis_config.instance.device.get_config_context() %}
"""
        footer = """
{% endfor %}
{# End of queryset iteration #}
{% else %}
{# Single object export - find the object in context #}
{% if isisconfiguration is defined %}
  {% set isis_config = isisconfiguration %}
{% elif obj is defined %}
  {% set isis_config = obj %}
{% elif object is defined %}
  {% set isis_config = object %}
{% endif %}
{% set interfaces = isis_config.interface_configurations.all %}
{% set device_config_context = isis_config.instance.device.get_config_context() %}
"""

        return wrapper + template_code + footer + "{% endif %}\n"

    def _wrap_ospf_template(self, template_code):
        """Wrap OSPF template for export template context."""
        # Export templates can be called from detail page (single object) or list page (queryset)
        wrapper = """{# Export Template Wrapper for OSPFConfiguration #}
{# Handle both single object and queryset export contexts #}
{% if queryset is defined %}
{# Queryset export - iterate over objects #}
{% for ospf_config in queryset %}
{% set interfaces = ospf_config.interface_configurations.all %}
{% set device_config_context = ospf_config.instance.device.get_config_context() %}
"""
        footer = """
{% endfor %}
{# End of queryset iteration #}
{% else %}
{# Single object export - find the object in context #}
{% if ospfconfiguration is defined %}
  {% set ospf_config = ospfconfiguration %}
{% elif obj is defined %}
  {% set ospf_config = obj %}
{% elif object is defined %}
  {% set ospf_config = object %}
{% endif %}
{% set interfaces = ospf_config.interface_configurations.all %}
{% set device_config_context = ospf_config.instance.device.get_config_context() %}
"""

        return wrapper + template_code + footer + "{% endif %}\n"
