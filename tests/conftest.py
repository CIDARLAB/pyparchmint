from parchmint.device import Device
from parchmint.component import Component
from parchmint.feature import Feature
import pytest
from parchmint import Layer


@pytest.fixture
def layer(layer_dict):
    return Layer(json_data=layer_dict)


@pytest.fixture
def device(layer):
    device = Device()
    device.add_layer(layer)
    return device


@pytest.fixture
def layer_dict(params_dict):
    ret = {
        "name": "flow_1",
        "id": "FLOW_1",
        "type": "FLOW",
        "group": "",
        "params": params_dict,
    }
    return ret


@pytest.fixture
def params_dict():
    ret = {
        "channelWidth": 1000,
        "rotation": 25,
        "position": [250, 300],
        "direction": "UP",
    }
    return ret


@pytest.fixture
def port_dict():
    ret = {"x": 0, "y": 0, "label": "1", "layer": "FLOW"}
    return ret


@pytest.fixture
def component_dict(port_dict, layer_dict, params_dict):
    layer = Layer(json_data=layer_dict)
    ret = {
        "name": "c1",
        "id": "c1",
        "entity": "MIXER",
        "layers": [layer.ID],
        "ports": [port_dict],
        "params": params_dict,
        "x-span": 1000,
        "y-span": 5000,
    }
    return ret


@pytest.fixture
def connection_target_dict():
    ret = {"component": "c1", "port": "1"}
    return ret


@pytest.fixture
def feature_dict(params_dict, layer_dict):
    layer = Layer(json_data=layer_dict)
    ret = {
        "id": "feat1",
        "type": "UNION",
        "macro": "TYPE1",
        "layerID": layer.ID,
        "params": params_dict,
    }
    return ret


@pytest.fixture
def connection_path_dict(connection_target_dict, feature_dict, layer, device):
    feature = Feature(json_data=feature_dict, device_ref=device)
    device.add_feature(feature)
    ret = {
        "source": connection_target_dict,
        "sink": connection_target_dict,
        "wayPoints": [[10, 10], [20, 20], [30, 30]],
        "features": [feature.ID],
    }
    return ret


@pytest.fixture
def connection_dict(
    params_dict, connection_path_dict, connection_target_dict, layer, feature_dict
):

    ret = {
        "source": connection_target_dict,
        "sinks": [connection_target_dict, connection_target_dict],
        "paths": [connection_path_dict, connection_path_dict],
        "layer": layer.ID,
        "id": "con1",
        "name": "con1",
        "entity": "CHANNEL",
        "params": params_dict,
    }
    return ret


@pytest.fixture
def valve1_dict(layer_dict, params_dict):
    return {
        "name": "valve1",
        "id": "valve1",
        "entity": "VALVE",
        "layers": [layer_dict["id"]],
        "ports": [{"x": 0, "y": 0, "label": "1", "layer": "CONTROL"}],
        "params": params_dict,
        "x-span": 1000,
        "y-span": 5000,
    }


@pytest.fixture
def valve2_dict(layer_dict, params_dict):
    return {
        "name": "valve2",
        "id": "valve2",
        "entity": "VALVE3D",
        "layers": [layer_dict["id"]],
        "ports": [{"x": 0, "y": 0, "label": "1", "layer": "CONTROL"}],
        "params": params_dict,
        "x-span": 1000,
        "y-span": 5000,
    }


@pytest.fixture
def device_dict(
    component_dict, connection_dict, feature_dict, layer_dict, valve1_dict, valve2_dict
):
    ret = {
        "name": "dev1",
        "params": {
            "x-span": 100000,
            "y-span": 50000,
        },
        "components": [
            component_dict,
            valve1_dict,
            valve2_dict,
        ],
        "connections": [connection_dict],
        "features": [feature_dict],
        "layers": [layer_dict],
        "valveMap": {
            "valve1": "con1",
            "valve2": "con1",
        },
        "valveTypeMap": {
            "valve1": "NORMALLY_OPEN",
            "valve2": "NORMALLY_CLOSED",
        },
        "version": "1.2",
    }
    return ret
