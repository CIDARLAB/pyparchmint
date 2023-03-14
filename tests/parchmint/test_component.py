import pytest

from parchmint import Component, Device, Layer, Params, Port


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
    component.add_component_port(top_port)
    component.add_component_port(bottom_port)

    return component


@pytest.fixture
def component2_for_rotation():
    component = Component()
    component.name = "c2"
    component.ID = "c2"
    component.entity = "MIXER"
    component.xspan = 1000
    component.yspan = 15000
    component.xpos = 2000
    component.ypos = 2000
    top_port = Port()
    top_port.label = "top"
    top_port.x = int(component.xspan / 2)
    top_port.y = 0
    bottom_port = Port()
    bottom_port.label = "bottom"
    bottom_port.x = int(component.xspan / 2)
    bottom_port.y = component.yspan
    component.add_component_port(top_port)
    component.add_component_port(bottom_port)

    return component


def test_get_component_spacing(component_for_rotation):
    # Should raise the exception since no component spacing is defined
    with pytest.raises(Exception) as e_info:
        component_spacing = component_for_rotation.component_spacing

    # Should set the component spacing
    component_for_rotation.params.set_param("componentSpacing", 2000)
    assert component_for_rotation.component_spacing == 2000


def test_set_component_spacing(component_for_rotation):
    # Set the component spacing
    component_for_rotation.component_spacing = 4000
    assert component_for_rotation.component_spacing == 4000


def test_to_parchmint_v1_2(params_dict, layer_dict, port_dict, component_dict):
    layer = Layer(json_data=layer_dict)
    device = Device()
    device.layers.append(layer)

    component = Component()
    component.name = "c1"
    component.ID = "c1"
    component.params = Params(params_dict)
    component.entity = "MIXER"
    component.layers.append(layer)
    component.add_component_port(Port(json_data=port_dict))
    component.xspan = 1000
    component.yspan = 5000
    # Test to see if the component dict is correct or not
    assert component.to_parchmint_v1() == component_dict


def test_from_parchmint_v1_2(layer_dict, component_dict):
    layer = Layer(json_data=layer_dict)
    device = Device()
    device.layers.append(layer)
    # Test to see if the loading from dictionary is working correctly
    # Create dummy device to get the layer id from
    component2 = Component.from_parchmint_v1_2(component_dict, device)
    assert component2.to_parchmint_v1() == component_dict


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


def test_get_rotated_component_definition(
    component_for_rotation, component2_for_rotation
):
    # Rotate the component
    rotated_component = component_for_rotation.get_rotated_component_definition(90)
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

    port = rotated_component.get_port("top")
    assert (port.x, port.y) == (15000, 500)
    port = rotated_component.get_port("bottom")
    assert (port.x, port.y) == (0, 500)

    # Its time to test this for a component with a non-0,0 position
    rotated_component = component2_for_rotation.get_rotated_component_definition(90)
    assert rotated_component.ports[0].x == component2_for_rotation.yspan
    assert rotated_component.ports[0].y == component2_for_rotation.xspan / 2
    assert rotated_component.ports[1].x == 0
    assert rotated_component.ports[1].y == component2_for_rotation.xspan / 2
    assert rotated_component.xspan == component2_for_rotation.yspan
    print("xspan:", component2_for_rotation.xspan)
    print("yspan:", component2_for_rotation.yspan)
    assert rotated_component.yspan == component2_for_rotation.xspan
    assert rotated_component.name == component2_for_rotation.name
    assert rotated_component.ID == component2_for_rotation.ID
    assert rotated_component.entity == component2_for_rotation.entity
    for key in component_for_rotation.params.data.keys():
        if key == "rotation":
            assert rotated_component.params.get_param(key) == 0
        elif key == "position":
            assert rotated_component.params.get_param(key) == [0, 0]
        else:
            assert rotated_component.params.get_param(
                key
            ) == component_for_rotation.params.get_param(key)


def test_rotate_point_around_center(component_for_rotation):
    component_for_rotation.xpos = 0
    component_for_rotation.ypos = 0
    rotated_point = component_for_rotation.rotate_point_around_center(1000, 0, 90)
    assert rotated_point == (8000, 8000)


def test_rotate_component(component_for_rotation, component2_for_rotation):
    component_for_rotation.xpos = 0
    component_for_rotation.ypos = 0
    # Check when the rotation is 0
    component_for_rotation.rotation = 0
    component_for_rotation.rotate_component()
    assert component_for_rotation.xpos == 0
    assert component_for_rotation.ypos == 0
    assert component_for_rotation.xspan == 1000
    assert component_for_rotation.yspan == 15000
    assert component_for_rotation.rotation == 0
    port = component_for_rotation.get_port("top")
    assert (port.x, port.y) == (500, 0)

    # now rotate the component and check
    old_rotation = 90
    component_for_rotation.rotation = old_rotation
    print("Top port: ", component_for_rotation.get_port("top"))
    component_for_rotation.rotate_component()
    assert component_for_rotation.xspan == 15000
    assert component_for_rotation.yspan == 1000
    assert component_for_rotation.xpos == -7000
    assert component_for_rotation.ypos == 7000
    assert component_for_rotation.rotation == old_rotation
    port = component_for_rotation.get_port("top")
    assert (port.x, port.y) == (15000, 500)

    # now test this for the non origin located component
    component2_for_rotation.rotation = 90
    # Save the old center coordinates
    old_xpos = component2_for_rotation.xpos + component2_for_rotation.xspan / 2
    old_ypos = component2_for_rotation.ypos + component2_for_rotation.yspan / 2
    component2_for_rotation.rotate_component()
    # First ensure that the center has not moved
    assert component2_for_rotation.xpos + component2_for_rotation.xspan / 2 == old_xpos
    assert component2_for_rotation.ypos + component2_for_rotation.yspan / 2 == old_ypos
    assert component2_for_rotation.xspan == 15000
    assert component2_for_rotation.yspan == 1000
    assert component2_for_rotation.xpos == -14000
    assert component2_for_rotation.ypos == 14000
    port = component2_for_rotation.get_port("top")
    assert (port.x, port.y) == (15000, 500)


def test_set_xpos_ypos(component_for_rotation):
    component_for_rotation.xpos = 1000
    component_for_rotation.ypos = 1000
    assert component_for_rotation.xpos == 1000
    assert component_for_rotation.ypos == 1000
