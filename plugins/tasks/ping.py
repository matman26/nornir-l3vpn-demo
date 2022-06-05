from nornir.core.task import Task, Result

def ping_address(task: Task, address: str, **kwargs) -> Result:
    net_connect = task.host.get_connection('netmiko', task.nornir.config)
    ping_data = net_connect.send_command(f"ping {address}", **kwargs)
    return Result(
        result=ping_data,
        changed=False,
        host=task.host)
