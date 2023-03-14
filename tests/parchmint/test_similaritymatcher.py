from parchmint.device import Device


def test_similarity_dx1_dx1():
    """
    Test the similarity matcher by comparing the dx1_ref.json file to itself.

    Comparision should be true.
    """

    # Load the dx1_ref test file
    device1 = None
    device2 = None
    with open("tests/data/dx1_ref.json", "r", encoding="utf-8") as file:
        text = file.read()
        device1 = Device.from_json(text)
        print(device1.name)

    # Load the dx1_ref test file again
    with open("tests/data/dx1_ref.json", "r", encoding="utf-8") as file:
        text = file.read()
        device2 = Device.from_json(text)
        print(device2.name)

    # Compare the two devices
    assert device1.compare(device=device2, compare_params=True) is True


def test_similarity_dx1_dx2():
    """
    Test the similarity matcher by comparing the dx1_ref.json file to dx2_ref.json.

    This comparision should be false.
    """
    # Load the dx1_ref test file
    device1 = None
    device2 = None
    with open("tests/data/dx1_ref.json", "r", encoding="utf-8") as file:
        text = file.read()
        device1 = Device.from_json(text)
        print(device1.name)

    # Load the dx1_ref test file again
    with open("tests/data/dx2_ref.json", "r", encoding="utf-8") as file:
        text = file.read()
        device2 = Device.from_json(text)
        print(device2.name)

    # Compare the two devices
    assert device1.compare(device=device2, compare_params=True) is False


def test_dx1_dx1_diff_entities():
    """
    Test where the same topology is used but have different entities

    Similarity should fail
    """
    # Load the dx1_ref test file
    device1 = None
    device2 = None
    with open("tests/data/dx1_ref.json", "r", encoding="utf-8") as file:
        text = file.read()
        device1 = Device.from_json(text)
        print(device1.name)

    # Load the dx1_ref test file again
    with open("tests/data/dx1__diff_entity_ref.json", "r", encoding="utf-8") as file:
        text = file.read()
        device2 = Device.from_json(text)
        print(device2.name)

    # Compare the two devices
    assert device1.compare(device=device2, compare_params=True) is False


def test_dx1_dx1_diff_params():
    """
    Test where the same topology and entities are used but have different parameters

    Similarity should fail
    """
    # Load the dx1_ref test file
    device1 = None
    device2 = None
    with open("tests/data/dx1_ref.json", "r", encoding="utf-8") as file:
        text = file.read()
        device1 = Device.from_json(text)
        print(device1.name)

    # Load the dx1_ref test file again
    with open("tests/data/dx1__diff_params_ref.json", "r", encoding="utf-8") as file:
        text = file.read()
        device2 = Device.from_json(text)
        print(device2.name)

    # Compare the two devices
    assert device1.compare(device=device2, compare_params=True) is False


def test_dx1_dx1_diff_ports():
    """
    Test where the same topology, entities and parameters are used but have different number of ports

    Similarity should fail
    """
    # Load the dx1_ref test file
    device1 = None
    device2 = None
    with open("tests/data/dx1_ref.json", "r", encoding="utf-8") as file:
        text = file.read()
        device1 = Device.from_json(text)
        print(device1.name)

    # Load the dx1_ref test file again
    with open("tests/data/dx1__diff_ports_ref.json", "r", encoding="utf-8") as file:
        text = file.read()
        device2 = Device.from_json(text)
        print(device2.name)

    # Compare the two devices
    assert device1.compare(device=device2, compare_params=True) is False


# TODO: Additional test cases for the similarity matcher
# 4. Test where the same topology, entities, parameters but have different port connections

# def test_dx1_dx1_diff_port_connections():
#     """
#     Test where the same topology, entities, parameters but have different port connections

#     Similarity should fail
#     """
#     # Load the dx1_ref test file
#     device1 = None
#     device2 = None
#     with open("tests/data/dx1_ref.json", "r", encoding="utf-8") as file:
#         text = file.read()
#         device1 = Device.from_json(text)
#         print(device1.name)

#     # Load the dx1_ref test file again
#     with open(
#         "tests/data/dx1__diff_port_connections_ref.json", "r", encoding="utf-8"
#     ) as file:
#         text = file.read()
#         device2 = Device.from_json(text)
#         print(device2.name)

#     # Compare the two devices
#     assert device1.compare(device=device2, compare_params=True) is False
