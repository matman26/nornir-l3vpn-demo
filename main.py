from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from plugins.tasks.template import apply_template
from nornir.core.filter import F
from nornir.core import Nornir
from nornir import InitNornir

def generate_apply_template(nr: Nornir, template_name: str, dry_run: bool) -> None:
    """
         Given a nornir object and a template name this generates all the
         templates for each host and proceeds to apply them if user
         confirms the action.
    """
    template_results = nr.run(
        name=f"Using template {template_name}",
        path='templates/',
        task=template_file,
        template=template_name,
    )

    # Prints generated templates
    print_result(template_results)

    # If executing in dry-run mode, ignore the next task
    if dry_run:
        return

    # === Requests user confirmation
    response = input("Dry-run above. Would you like to apply changes? [y/N] ")
    if response not in ['y', 'Y']:
        return

    config_results = nr.run(
        name=f"Applying generated configs for {template_name}",
        task=apply_template,
        results=template_results
    )

    # Prints execution results
    print_result(config_results)

# ==============================
# === BEGIN SCRIPT EXECUTION ===
# ==============================
if __name__ == "__main__":
    # === Initializes Nornir
    # === Loads in configuration file
    nr = InitNornir(config_file="config.yaml")

    # === Dry-run mode
    dry_run = False

    # === Filter the inventory for PE routers only
    pe_routers = nr.filter(F(groups__contains="PE"))

    # =======================
    # === Apply templates ===
    # =======================

    # ==== Client VRF Configuration
    # ====  This template creates the customer VRF instance
    # ====  and links that to a physical interface on the router.
    generate_apply_template(pe_routers, 'ios_vrf_add.j2'           , dry_run)

    # ==== MP-BGP Configuration
    # ====  This template creates an MP-BGP neighborship between peer
    # ====  PE routers as specified in the data model.
    generate_apply_template(pe_routers, 'ios_bgp_vpnv4_add.j2'     , dry_run)

    # ==== PE-CE OSPF Configuration
    # ====  This template creates an OSPF neighborship between the PE
    # ====  (provider edge) and CE (customer edge) routers.
    generate_apply_template(pe_routers, 'ios_ospf_pe_add.j2'       , dry_run)

    # ==== Redistribution configuration
    # ====  This templates creates the redistribution from OSPF to BGP
    # ====  and from BGP to OSPF
    generate_apply_template(pe_routers, 'ios_redistribution_add.j2', dry_run)
