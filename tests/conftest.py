from parchmint.feature import Feature
import pytest
from parchmint import Layer


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
def feature_dict(params_dict):
    ret = {"id": "feat1", "type": "UNION", "macro": "TYPE1", "params": params_dict}
    return ret


@pytest.fixture
def connection_path_dict(connection_target_dict, feature_dict):
    feature = Feature(json_data=feature_dict)
    ret = {
        "source": connection_target_dict,
        "sink": connection_target_dict,
        "wayPoints": [[10, 10], [20, 20], [30, 30]],
        "features": [feature.ID],
    }
    return ret


@pytest.fixture
def connection_dict(
    params_dict, connection_path_dict, connection_target_dict, layer_dict, feature_dict
):
    layer = Layer(json_data=layer_dict)
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
