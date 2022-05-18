from parchmint.device import ValveType
from parchmint.feature import Feature
from parchmint.layer import Layer
from parchmint.component import Component
from parchmint.connection import Connection
from parchmint import Device


def test_to_parchmint_v1_x(
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
    device.add_feature(Feature(json_data=feature_dict, device_ref=device))
    con1 = Connection(json_data=connection_dict, device_ref=device)
    device.add_connection(con1)
    device.add_component(Component(json_data=component_dict, device_ref=device))
    valve1 = Component(json_data=valve1_dict, device_ref=device)
    valve2 = Component(json_data=valve2_dict, device_ref=device)
    device.add_component(valve1)
    device.add_component(valve2)
    device.map_valve(valve1, con1, ValveType.NORMALLY_OPEN)
    device.map_valve(valve2, con1, ValveType.NORMALLY_CLOSED)
    assert device.to_parchmint_v1_x() == device_dict
