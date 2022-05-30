import pytest

from parchmint import Device
from parchmint.component import Component
from parchmint.connection import Connection
from parchmint.device import ValveType
from parchmint.feature import Feature
from parchmint.layer import Layer
from parchmint.target import Target


@pytest.fixture
def temp_device():
    device = Device()
    device.name = "dev1"
    device.xspan = 100000
    device.yspan = 50000

    return device


def test_add_feature(temp_device, feature_dict, layer_dict):
    temp_device.add_layer(Layer(json_data=layer_dict))
    feature = Feature.from_parchmint_v1_2(
        json_data=feature_dict, device_ref=temp_device
    )
    temp_device.add_feature(feature)
    assert feature in temp_device.features


def test_remove_feature(temp_device, feature_dict, layer_dict):
    temp_device.add_layer(Layer(json_data=layer_dict))
    feature = Feature.from_parchmint_v1_2(
        json_data=feature_dict, device_ref=temp_device
    )
    temp_device.add_feature(feature)
    temp_device.remove_feature(feature.ID)
    assert feature not in temp_device.features
    assert temp_device.graph.has_node(feature.ID) is False


def test_add_compoent(temp_device, component_dict, layer_dict):
    temp_device.add_layer(Layer(json_data=layer_dict))
    component = Component.from_parchmint_v1_2(
        json_data=component_dict, device_ref=temp_device
    )
    temp_device.add_component(component)
    assert component in temp_device.components
    assert temp_device.graph.has_node(component.ID)


def test_remove_component(temp_device, component_dict, layer_dict):
    temp_device.add_layer(Layer(json_data=layer_dict))
    component = Component.from_parchmint_v1_2(
        json_data=component_dict, device_ref=temp_device
    )
    temp_device.add_component(component)
    temp_device.remove_component(component.ID)
    assert component not in temp_device.components
    assert temp_device.graph.has_node(component.ID) is False


def test_add_connection(
    temp_device, component_dict, pathless_connection_dict, connection_dict, layer_dict
):
    # Ideal scenario for this test, has all the components already present in the graph before inserting the connection
    temp_device.add_layer(Layer(json_data=layer_dict))
    component1 = Component.from_parchmint_v1_2(
        json_data=component_dict, device_ref=temp_device
    )
    component2 = Component.from_parchmint_v1_2(
        json_data=component_dict, device_ref=temp_device
    )
    component2.ID = "c2"
    component2.name = "c2"

    connection1 = Connection.from_parchmint_v1_2(
        json_data=pathless_connection_dict, device_ref=temp_device
    )
    connection1.ID = "connection1"
    source_target = Target()
    source_target.component = component1.ID
    source_target.port = "1"
    connection1.source = source_target

    sink_target = Target()
    sink_target.component = component2.ID
    sink_target.port = "1"
    connection1.sinks.append(sink_target)

    # First test to see if this raises an exception when there are no source and sink components added to the device
    with pytest.raises(Exception):
        temp_device.add_connection(connection1)

    # Now add the source and see if it raises an exception
    with pytest.raises(Exception):
        temp_device.add_component(component1)
        temp_device.add_connection(connection1)

    # Now add the sink and see if it goes through without raising an exception
    temp_device.add_component(component2)
    temp_device.add_connection(connection1)

    assert connection1 in temp_device.connections
    assert temp_device.graph.has_edge(component1.ID, component2.ID)


def test_remove_connection(temp_device, layer_dict, component_dict):
    temp_device.add_layer(Layer(json_data=layer_dict))
    component1 = Component.from_parchmint_v1_2(
        json_data=component_dict, device_ref=temp_device
    )
    temp_device.add_component(component1)
    component2 = Component.from_parchmint_v1_2(
        json_data=component_dict, device_ref=temp_device
    )
    component2.ID = "c2"
    component2.name = "c2"
    temp_device.add_component(component2)

    connection1 = Connection()
    connection1.ID = "connection1"
    source_target = Target()
    source_target.component = component1.ID
    source_target.port = "1"
    connection1.source = source_target

    sink_target = Target()
    sink_target.component = component2.ID
    sink_target.port = "1"
    connection1.sinks.append(sink_target)

    temp_device.add_connection(connection1)

    temp_device.remove_connection(connection1.ID)

    assert connection1 not in temp_device.connections
    assert temp_device.graph.has_edge(component1.ID, component2.ID) is False


def test_get_connections_for_edge(temp_device, layer_dict, component_dict):
    temp_device.add_layer(Layer(json_data=layer_dict))
    component1 = Component.from_parchmint_v1_2(
        json_data=component_dict, device_ref=temp_device
    )
    temp_device.add_component(component1)
    component2 = Component.from_parchmint_v1_2(
        json_data=component_dict, device_ref=temp_device
    )
    component2.ID = "c2"
    component2.name = "c2"
    temp_device.add_component(component2)

    connection1 = Connection()
    connection1.ID = "connection1"
    source_target = Target()
    source_target.component = component1.ID
    source_target.port = "1"
    connection1.source = source_target

    sink_target = Target()
    sink_target.component = component2.ID
    sink_target.port = "1"
    connection1.sinks.append(sink_target)

    temp_device.add_connection(connection1)

    connection2 = Connection()
    connection2.ID = "connection2"
    source_target = Target()
    source_target.component = component1.ID
    source_target.port = "2"
    connection2.source = source_target

    sink_target = Target()
    sink_target.component = component2.ID
    sink_target.port = "2"
    connection2.sinks.append(sink_target)

    temp_device.add_connection(connection2)

    assert temp_device.get_connections_for_edge(component1, component2) == [
        connection1,
        connection2,
    ]

    assert temp_device.get_connections_for_edge(component2, component1) == []


def test_to_parchmint_v1_2(
    device_dict,
    connection_dict,
    component_dict,
    layer_dict,
    feature_dict,
    valve1_dict,
    valve2_dict,
):
    device = Device()
    device.name = "dev1"
    device.xspan = 100000
    device.yspan = 50000
    device.add_layer(Layer(json_data=layer_dict))
    device.add_feature(
        Feature.from_parchmint_v1_2(json_data=feature_dict, device_ref=device)
    )

    device.add_component(
        Component.from_parchmint_v1_2(json_data=component_dict, device_ref=device)
    )
    con1 = Connection.from_parchmint_v1_2(json_data=connection_dict, device_ref=device)
    device.add_connection(con1)
    valve1 = Component.from_parchmint_v1_2(json_data=valve1_dict, device_ref=device)
    valve2 = Component.from_parchmint_v1_2(json_data=valve2_dict, device_ref=device)
    device.add_component(valve1)
    device.add_component(valve2)
    device.map_valve(valve1, con1, ValveType.NORMALLY_OPEN)
    device.map_valve(valve2, con1, ValveType.NORMALLY_CLOSED)
    assert device.to_parchmint_v1_2() == device_dict


def test_from_parchmint_v1_2(device_dict):
    device = Device.from_parchmint_v1_2(json_data=device_dict)
    assert device.to_parchmint_v1_2() == device_dict
