import json

from parchmint.device import Device


def test_similarity_dx1_dx1():
    # Load the dx1_ref test file
    device1 = None
    device2 = None
    with open("tests/data/dx1_ref_no_par.json", "r", encoding="utf-8") as f:
        text = f.read()
        device1 = Device.from_json(text)
        print(device1.name)

    # Load the dx1_ref test file again
    with open("tests/data/dx1_ref_no_par.json", "r", encoding="utf-8") as f:
        text = f.read()
        device2 = Device.from_json(text)
        print(device2.name)
    
    # Compare the two devices
    assert device1.compare(device=device2, compare_params=True) is True

def test_similarity_dx1_dx2():
    # Load the dx1_ref test file
    device1 = None
    device2 = None
    with open("tests/data/dx1_ref_no_par.json", "r" , encoding="utf-8") as f:
        text = f.read()
        device1 = Device.from_json(text)
        print(device1.name)

    # Load the dx1_ref test file again
    with open("tests/data/dx8_ref_no_par.json", "r", encoding="utf-8") as f:
        text = f.read()
        device2 = Device.from_json(text)
        print(device2.name)
    
    # Compare the two devices
    assert device1.compare(device=device2, compare_params=True) is False
    

        