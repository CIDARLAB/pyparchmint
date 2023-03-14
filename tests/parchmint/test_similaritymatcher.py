import json

from parchmint.device import Device


def test_similarity_dx1_dx1():
    # Load the dx1_ref test file
    device1 = None
    device2 = None
    with open("tests/data/dx1_ref.json", "r") as f:
        json_text = json.load(f)
        device_json = json.loads(json_text)
        device1 = Device.from_json(device_json)

    # Load the dx1_ref test file again
    with open("tests/data/dx1_ref.json", "r") as f:
        json_text = json.load(f)
        device_json = json.loads(json_text)
        device2 = Device.from_json(device_json)
    
    # Compare the two devices
    assert device1.compare(device=device2, compare_params=True) is True

def test_similarity_dx1_dx2():
    # Load the dx1_ref test file
    device1 = None
    device2 = None
    with open("tests/data/dx1_ref.json", "r") as f:
        json_text = json.load(f)
        device_json = json.loads(json_text)
        device1 = Device.from_json(device_json)

    # Load the dx1_ref test file again
    with open("tests/data/dx2_ref.json", "r") as f:
        json_text = json.load(f)
        device_json = json.loads(json_text)
        device2 = Device.from_json(device_json)
    
    # Compare the two devices
    assert device1.compare(device=device2, compare_params=True) is False
    

        