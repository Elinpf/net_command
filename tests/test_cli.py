import json
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture
def inventory_file():
    return "tests/inventory.yaml"


@pytest.fixture
def playbook_file():
    return "tests/playbook.yaml"


def test_list_inventory(inventory_file):
    result = subprocess.run(
        [sys.executable, "-m", "net_command.cli", "-i", inventory_file, "--list"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    inventory = json.loads(result.stdout)
    assert isinstance(inventory, dict)
    assert "_meta" in inventory
    assert "hostvars" in inventory["_meta"]


def test_execute_playbook(inventory_file, playbook_file):
    result = subprocess.run(
        [sys.executable, "-m", "net_command.cli", "-i", inventory_file, playbook_file],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "H3C NTP Configuration" in result.stdout
