import pytest

from net_command import execute_playbook, load_inventory, load_playbook, print_output
from net_command.playbook import replace_placeholders


@pytest.fixture
def inventory_file():
    return "tests/inventory.yaml"


@pytest.fixture
def playbook_file():
    return "tests/playbook.yaml"


@pytest.fixture
def devices(inventory_file):
    return load_inventory(inventory_file)


@pytest.fixture
def playbook(playbook_file):
    return load_playbook(playbook_file)


def test_load_inventory(inventory_file):
    inventory = load_inventory(inventory_file)
    assert isinstance(inventory, dict)
    assert "_meta" in inventory
    assert "hostvars" in inventory["_meta"]
    assert len(inventory["_meta"]["hostvars"]) > 0


def test_load_playbook(playbook_file):
    playbook = load_playbook(playbook_file)
    assert isinstance(playbook, list)
    assert len(playbook) > 0
    assert "tasks" in playbook[0]


def test_execute_playbook(devices, playbook):
    results = execute_playbook(devices, playbook)
    assert isinstance(results, dict)
    assert len(results) > 0


def test_print_output(devices, playbook):
    results = execute_playbook(devices, playbook)
    print_output(results)


def test_when_condition_not_met(inventory_file):
    inventory = load_inventory(inventory_file)
    playbook = [
        {
            "name": "Test when condition not met",
            "hosts": "box_as",
            "num_processes": 2,
            "tasks": [
                {
                    "name": "This task should not run",
                    "when": "vendor == 'non_existent_vendor'",
                    "commands": ["display ntp status"],
                }
            ],
        }
    ]
    results = execute_playbook(inventory, playbook)
    assert "Test when condition not met" not in results


def test_replace_placeholders():
    variables = {
        "host": "192.168.56.2",
        "port": 22,
        "user": "admin",
        "password": "password@123456",
    }
    text = "Device settings: hp_comware {{ host }}:{{ port }}"
    expected = "Device settings: hp_comware 192.168.56.2:22"
    assert replace_placeholders(text, variables) == expected

    text_list = ["Connect to {{ host }}", "Port: {{ port }}"]
    expected_list = ["Connect to 192.168.56.2", "Port: 22"]
    assert replace_placeholders(text_list, variables) == expected_list

    text_dict = {"host": "{{ host }}", "port": "{{ port }}"}
    expected_dict = {"host": "192.168.56.2", "port": "22"}
    assert replace_placeholders(text_dict, variables) == expected_dict
