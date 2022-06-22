from nornir.core.task import Task, Result, MultiResult

def apply_template(task: Task, results: MultiResult) -> Result:
    # === Loads the templated configuration from the device's
    # === result attribute
    template   = results[task.host.name].result

    # === Transforms template lines into a list of strings
    # === (compatible with netmiko's send_config_set)
    config_set = template.splitlines()

    # === Initializes a Netmiko connection to the device
    connection = task.host.get_connection('netmiko', task.nornir.config)

    # === Checks if the connection is alive. If not, establish
    # === a new one
    if not connection.is_alive():
        connection.establish_connection()

    # === Enters the device's enable and config mode (for cisco)
    connection.enable()
    connection.config_mode()

    # === Sends the templated configuration to the device
    result_data = connection.send_config_set(config_set)

    # === Disconnects the remote session
    connection.disconnect()

    # === Returns execution results
    return Result(
        result=result_data,
        host=task.host,
        changed=True
    )
