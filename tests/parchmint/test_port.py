from parchmint import Port


def test_port_to_parchmint_v1_x_dict(port_dict):
    port = Port()
    port.x = 0
    port.y = 0
    port.label = "1"
    port.layer = "FLOW"
    assert port.to_parchmint_v1() == port_dict

    # Test to see if the loading from dictionary is working correctly
    port = Port(json_data=port_dict)
    assert port.to_parchmint_v1() == port_dict
