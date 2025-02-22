import re

import yaml

from .parallel_executor import run_tasks


def load_playbook(file_path):
    with open(file_path, "r") as file:
        playbook = yaml.safe_load(file)
    return playbook


def replace_placeholders(text, variables):
    pattern = re.compile(r"{{\s*(\w+)\s*}}")
    if isinstance(text, str):
        return pattern.sub(
            lambda match: str(variables.get(match.group(1), match.group(0))), text
        )
    elif isinstance(text, list):
        return [replace_placeholders(item, variables) for item in text]
    elif isinstance(text, dict):
        return {k: replace_placeholders(v, variables) for k, v in text.items()}
    return text


def execute_playbook(inventory, playbook):
    results = {}
    for task in playbook:
        task_name = task["name"]
        hosts = task["hosts"]
        task_vars = task.get("vars", {})
        devices = []
        if hosts == "all":
            host_list = [
                host
                for group in inventory
                if group != "_meta"
                for host in inventory[group].get("hosts", [])
            ]
        else:
            host_list = inventory[hosts]["hosts"]
        for host in host_list:
            host_vars = inventory["_meta"]["hostvars"][host]
            if any(eval(sub_task["when"], {}, host_vars) for sub_task in task["tasks"]):
                host_vars["host"] = host
                device = {
                    "device_type": host_vars["vendor"],
                    "host": host,
                    "username": host_vars["user"],
                    "password": host_vars["password"],
                    "port": int(host_vars["port"]),
                }
                device.update(replace_placeholders(task_vars, host_vars))
                devices.append(device)
        if devices:
            for sub_task in task["tasks"]:
                if eval(sub_task["when"], {}, host_vars):
                    command = {}
                    if "display_commands" in sub_task:
                        command["display_commands"] = replace_placeholders(
                            sub_task["display_commands"], host_vars
                        )
                    if "config_commands" in sub_task:
                        command["config_commands"] = replace_placeholders(
                            sub_task["config_commands"], host_vars
                        )
                    task_results = run_tasks(
                        devices, command, task.get("num_processes", 4)
                    )
                    results[f"{task_name} - {sub_task['name']}"] = task_results
    return results
