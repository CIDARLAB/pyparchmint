from parchmint import Component, Device, Layer, Params, Port
import pytest


@pytest.fixture
def component_for_rotation():
    component = Component()
    component.name = "c1"
    component.ID = "c1"
    component.entity = "MIXER"
    component.xspan = 1000
    component.yspan = 15000
    top_port = Port()
    top_port.label = "top"
    top_port.x = int(component.xspan / 2)
    top_port.y = 0
    bottom_port = Port()
    bottom_port.label = "bottom"
    bottom_port.x = int(component.xspan / 2)
    bottom_port.y = component.yspan
    component.ports.append(top_port)
    component.ports.append(bottom_port)

    return component


def test_component_to_parchmint_v1_x_dict(
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
    component = Component(json_data=component_dict, device_ref=device)
    assert component.to_parchmint_v1() == component_dict


def test_rotate_point(component_for_rotation):
    # Create a component with ports on the top and bottom
    top_port = component_for_rotation.ports[0]
    bottom_port = component_for_rotation.ports[1]
    # Rotate the component
    new_coordinates = component_for_rotation.rotate_point(top_port.x, top_port.y, 90)
    assert new_coordinates == (
        component_for_rotation.yspan,
        component_for_rotation.xspan / 2,
    )
    new_coordinates = component_for_rotation.rotate_point(
        bottom_port.x, bottom_port.y, 90
    )
    assert new_coordinates == (0, component_for_rotation.xspan / 2)


def test_rotate_component(component_for_rotation):
    # Rotate the component
    rotated_component = component_for_rotation.get_rotated_component(90)
    assert rotated_component.ports[0].x == component_for_rotation.yspan
    assert rotated_component.ports[0].y == component_for_rotation.xspan / 2
    assert rotated_component.ports[1].x == 0
    assert rotated_component.ports[1].y == component_for_rotation.xspan / 2
    assert rotated_component.xspan == component_for_rotation.yspan
    print("xspan:", component_for_rotation.xspan)
    print("yspan:", rotated_component.yspan)
    assert rotated_component.yspan == component_for_rotation.xspan
    assert rotated_component.name == component_for_rotation.name
    assert rotated_component.ID == component_for_rotation.ID
    assert rotated_component.entity == component_for_rotation.entity
    for key in component_for_rotation.params.data.keys():
        if key == "rotation":
            assert rotated_component.params.get_param(key) == 0
        else:
            assert rotated_component.params.get_param(
                key
            ) == component_for_rotation.params.get_param(key)
