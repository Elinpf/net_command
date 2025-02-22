from __future__ import annotations

import os
from multiprocessing import Pool

from netmiko import ConnectHandler


def execute_task(device_command_pair):
    device, command = device_command_pair
    os.makedirs("logs", exist_ok=True)  # 确保 logs 目录存在
    device["session_log"] = (
        f"logs/{device['host']}_session.log"  # 日志统一放在 logs/ 目录下
    )
    connection = ConnectHandler(**device)
    if isinstance(command, dict):
        output = []
        if "display_commands" in command:
            output.extend(
                [connection.send_command(cmd) for cmd in command["display_commands"]]
            )
        if "config_commands" in command:
            output.append(connection.send_config_set(command["config_commands"]))
    else:
        output = connection.send_command(command)
    connection.disconnect()
    return output


def run_tasks(devices, command, num_processes):
    with Pool(processes=num_processes) as pool:
        results = []
        for i, result in enumerate(
            pool.imap_unordered(execute_task, [(device, command) for device in devices])
        ):
            results.append(result)
            print(f"Progress: {i + 1}/{len(devices)} tasks completed")
    return results
