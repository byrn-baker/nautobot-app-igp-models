"""Management command to analyze and suggest default values for IGP configurations."""

from collections import Counter

from django.core.management.base import BaseCommand
from django.db.models import Count, Q

from nautobot_igp_models.models import (
    ISISConfiguration,
    ISISInterfaceConfiguration,
    OSPFConfiguration,
    OSPFInterfaceConfiguration,
)


class Command(BaseCommand):
    """Analyze interface configurations and suggest default values."""

    help = "Analyze existing interface configurations and suggest default values for IGP configs"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Apply suggested defaults (otherwise just show recommendations)",
        )
        parser.add_argument(
            "--protocol",
            choices=["isis", "ospf", "both"],
            default="both",
            help="Which protocol to analyze (default: both)",
        )
        parser.add_argument(
            "--min-interfaces",
            type=int,
            default=2,
            help="Minimum number of interfaces to suggest defaults (default: 2)",
        )

    def handle(self, *args, **options):
        """Execute the command."""
        apply = options["apply"]
        protocol = options["protocol"]
        min_interfaces = options["min_interfaces"]

        if protocol in ["isis", "both"]:
            self.analyze_isis(apply=apply, min_interfaces=min_interfaces)

        if protocol in ["ospf", "both"]:
            self.analyze_ospf(apply=apply, min_interfaces=min_interfaces)

    def analyze_isis(self, apply=False, min_interfaces=2):
        """Analyze ISIS configurations and suggest defaults."""
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("ISIS Configuration Analysis"))
        self.stdout.write("=" * 70 + "\n")

        isis_configs = ISISConfiguration.objects.annotate(
            interface_count=Count("interface_configurations")
        ).filter(interface_count__gte=min_interfaces)

        if not isis_configs.exists():
            self.stdout.write(
                self.style.WARNING(
                    f"No ISIS configurations found with at least {min_interfaces} interfaces"
                )
            )
            return

        for isis_config in isis_configs:
            self.stdout.write(f"\nAnalyzing: {isis_config.name}")
            self.stdout.write(f"Device: {isis_config.instance.device.name}")
            self.stdout.write(f"Interfaces: {isis_config.interface_count}")

            interfaces = isis_config.interface_configurations.all()

            # Analyze metrics
            metrics = [i.metric for i in interfaces if i.metric is not None]
            if metrics:
                metric_counts = Counter(metrics)
                most_common_metric, count = metric_counts.most_common(1)[0]

                if count >= min_interfaces:
                    self.stdout.write(
                        f"  → Suggested default_metric: {most_common_metric} "
                        f"(used by {count}/{len(interfaces)} interfaces)"
                    )

                    if apply:
                        if isis_config.default_metric is None:
                            isis_config.default_metric = most_common_metric
                            isis_config.save()
                            self.stdout.write(
                                self.style.SUCCESS("    ✓ Applied default_metric")
                            )

                            # Clear metric from interfaces that match default
                            interfaces.filter(metric=most_common_metric).update(
                                metric=None
                            )
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"    ✓ Cleared metric from {count} interfaces (now inherit default)"
                                )
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"    ⊘ Already has default_metric={isis_config.default_metric}"
                                )
                            )
                else:
                    self.stdout.write(
                        f"  → No clear consensus on metric (most common: {most_common_metric} used {count} times)"
                    )
            else:
                self.stdout.write("  → No explicit metrics set")

            # Show current defaults
            if isis_config.default_metric:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  Current defaults: metric={isis_config.default_metric}"
                    )
                )

    def analyze_ospf(self, apply=False, min_interfaces=2):
        """Analyze OSPF configurations and suggest defaults."""
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("OSPF Configuration Analysis"))
        self.stdout.write("=" * 70 + "\n")

        ospf_configs = OSPFConfiguration.objects.annotate(
            interface_count=Count("interface_configurations")
        ).filter(interface_count__gte=min_interfaces)

        if not ospf_configs.exists():
            self.stdout.write(
                self.style.WARNING(
                    f"No OSPF configurations found with at least {min_interfaces} interfaces"
                )
            )
            return

        for ospf_config in ospf_configs:
            self.stdout.write(f"\nAnalyzing: {ospf_config.name}")
            self.stdout.write(f"Device: {ospf_config.instance.device.name}")
            self.stdout.write(f"Process ID: {ospf_config.process_id}")
            self.stdout.write(f"Interfaces: {ospf_config.interface_count}")

            interfaces = ospf_config.interface_configurations.all()

            # Analyze costs
            costs = [i.cost for i in interfaces if i.cost is not None]
            if costs:
                cost_counts = Counter(costs)
                most_common_cost, count = cost_counts.most_common(1)[0]

                if count >= min_interfaces:
                    self.stdout.write(
                        f"  → Suggested default_cost: {most_common_cost} "
                        f"(used by {count}/{len(interfaces)} interfaces)"
                    )

                    if apply:
                        if ospf_config.default_cost is None:
                            ospf_config.default_cost = most_common_cost
                            ospf_config.save()
                            self.stdout.write(
                                self.style.SUCCESS("    ✓ Applied default_cost")
                            )

                            # Clear cost from interfaces that match default
                            interfaces.filter(cost=most_common_cost).update(cost=None)
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"    ✓ Cleared cost from {count} interfaces (now inherit default)"
                                )
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"    ⊘ Already has default_cost={ospf_config.default_cost}"
                                )
                            )
                else:
                    self.stdout.write(
                        f"  → No clear consensus on cost (most common: {most_common_cost} used {count} times)"
                    )
            else:
                self.stdout.write("  → No explicit costs set")

            # Show current defaults
            if ospf_config.default_cost:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  Current defaults: cost={ospf_config.default_cost}"
                    )
                )

        self.stdout.write("\n" + "=" * 70)
        if not apply:
            self.stdout.write(
                self.style.WARNING(
                    "\nℹ  This was a dry-run. Use --apply to actually update configurations."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "\n✓ Analysis complete. Defaults applied where appropriate."
                )
            )
        self.stdout.write("=" * 70 + "\n")
