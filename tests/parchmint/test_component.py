from parchmint import Component, Layer, Port, Params, Device


def test_component_to_parchmint_v1_2(
    params_dict, layer_dict, port_dict, component_dict
):
    layer = Layer(layer_dict)
    component = Component()
    component.name = "c1"
    component.ID = "c1"
    component.params = Params(params_dict)
    component.entity = "MIXER"
    component.layers.append(layer)
    component.ports.append(Port(port_dict))
    component.xspan = 1000
    component.yspan = 5000
    # Test to see if the component dict is correct or not
    assert component.to_parchmint_v1() == component_dict

    # Test to see if the loading from dictionary is working correctly
    # Create dummy device to get the layer id from
    device = Device()
    device.layers.append(layer)
    component = Component.from_parchmint_v1_2(component_dict, device)
    assert component.to_parchmint_v1() == component_dict
