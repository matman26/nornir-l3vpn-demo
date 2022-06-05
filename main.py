from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from plugins.tasks.template import apply_template
from nornir.core.filter import F
from nornir.core import Nornir
from nornir import InitNornir

def generate_apply_template(nr: Nornir, template_name: str, dry_run: bool):
    template_results = nr.run(
        name=f"Usando template {template_name}",
        path='templates/',
        task=template_file,
        template=template_name,
    )
    print_result(template_results)

    if not dry_run:
        config_results = nr.run(
            name=f"Aplicando configuracoes geradas {template_name}",
            task=apply_template,
            results=template_results
        )
        print_result(config_results)

# === INICIO DE EXECUCAO DO SCRIPT
if __name__ == "__main__":
    # === Inicializa Nornir, carrega inventario,
    # === carrega arquivo de configuracao
    nr = InitNornir(config_file="config.yaml")

    # === Dry-run mode
    dry_run = False

    # === Filtra o Inventario para apenas membros
    # === do grupo PE
    pe_routers = nr.filter(F(groups__contains="PE"))

    # === Aplicar templates
    generate_apply_template(pe_routers, 'ios_vrf_add.j2'           , dry_run)
    generate_apply_template(pe_routers, 'ios_bgp_vpnv4_add.j2'     , dry_run)
    generate_apply_template(pe_routers, 'ios_ospf_pe_add.j2'       , dry_run)
    generate_apply_template(pe_routers, 'ios_redistribution_add.j2', dry_run)
