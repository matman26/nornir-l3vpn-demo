from nornir.core.task import Task, Result, MultiResult

def apply_template(task: Task, results: MultiResult) -> Result:
    # === Carrega o TEMPLATE em memoria do dicionario com resultados
    template   = results[task.host.name].result

    # === Transforma as linhas do template em uma lista de strings
    # === (compativel com o send_config_set)
    config_set = [ config.strip() for config in template.split('\n') ]

    # === Inicializa uma conexao NETMIKO com o device
    connection = task.host.get_connection('netmiko', task.nornir.config)

    # === Checa se a conexao esta morta, se estiver, reconecta
    if not connection.is_alive():
        connection.establish_connection()

    # === Habilita Enable da caixa e modo de Config
    connection.enable()
    connection.config_mode()

    # === Envia configuracao templatizada ao device
    result_data = connection.send_config_set(config_set)

    # === Desconecta a sessao remota
    connection.disconnect()

    # === Retorna o resultado no formato convencional
    return Result(
        result=result_data,
        host=task.host,
        changed=True
    )
