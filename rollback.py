from main import generate_apply_template
from nornir.core.filter import F
from nornir import InitNornir

def rollback() -> None:
    # === Initializes Nornir
    # === Loads in configuration file
    nr = InitNornir(config_file="config.yaml")

    # === Dry-run mode
    dry_run = False

    # === Filter the inventory for PE routers only
    pe_routers = nr.filter(F(groups__contains="PE"))

    # =======================
    # === Rollback prompt ===
    # =======================
    print("================================================================")
    rollback = input("================ Are you sure you want to Rollback? [y/N] ")
    print("================================================================")

    if rollback not in ('Y', 'y'):
        return

    # === Rollback
    # ==== Redistribution Rollback
    generate_apply_template(pe_routers, 'ios_redistribution_del.j2', dry_run)

    # ==== OSPF Rollback
    generate_apply_template(pe_routers, 'ios_ospf_pe_del.j2'       , dry_run)

    # ==== MP-BGP Rollback
    generate_apply_template(pe_routers, 'ios_bgp_vpnv4_del.j2'     , dry_run)

    # ==== VRF Rollback
    generate_apply_template(pe_routers, 'ios_vrf_del.j2'           , dry_run)

# ==============================
# === BEGIN SCRIPT EXECUTION ===
# ==============================
if __name__ == "__main__":
    rollback()
