import pytest

from net_command.inventory import load_inventory
from net_command.playbook import execute_playbook, load_playbook


@pytest.fixture
def inventory():
    return load_inventory("tests/inventory.yaml")


@pytest.fixture
def playbook():
    return load_playbook("tests/playbook.yaml")


def test_execute_playbook_all_hosts(inventory, playbook):
    results = execute_playbook(inventory, playbook)
    assert "H3C NTP Configuration - Display H3C Commands" in results
    assert "H3C NTP Configuration - H3C Config Commands" in results
    assert len(results["H3C NTP Configuration - Display H3C Commands"]) == 3
    assert len(results["H3C NTP Configuration - H3C Config Commands"]) == 3
