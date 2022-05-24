from parchmint import Connection, ConnectionPath
from parchmint.device import Device
from parchmint.feature import Feature
from parchmint.layer import Layer
from parchmint.params import Params
from parchmint.target import Target

# TODO- Create test cases for a connection constructor and see whether it fails for for routed connection if the features are not present in the constructor


def test_connectionPath_to_parchmint_v1(
    connection_target_dict, connection_path_dict, feature_dict, device
):
    feat1 = Feature.from_parchmint_v1_2(json_data=feature_dict, device_ref=device)
    device.add_feature(feat1)

    cp = ConnectionPath(
        source=Target(json_data=connection_target_dict),
        sink=Target(json_data=connection_target_dict),
        waypoints=[(10, 10), (20, 20), (30, 30)],
        features=[feat1],
    )
    assert cp.to_parchmint_v1_2() == connection_path_dict


def test_connectionPath_parse_parchmint_v1(connection_path_dict, feature_dict, device):
    feat1 = Feature.from_parchmint_v1_2(json_data=feature_dict, device_ref=device)
    device.features = [feat1]

    cp = ConnectionPath.from_parchmint_v1_2(connection_path_dict, device)
    assert cp.to_parchmint_v1_2() == connection_path_dict


def test_connection_to_parchmint_v1_2(
    layer_dict,
    connection_target_dict,
    connection_path_dict,
    params_dict,
    feature_dict,
    connection_dict,
):
    layer = Layer(json_data=layer_dict)

    device = Device()
    device.add_layer(layer)
    feat = Feature.from_parchmint_v1_2(json_data=feature_dict, device_ref=device)
    device.add_feature(feat)
    c = Connection()
    c.ID = "con1"
    c.name = "con1"
    c.source = Target(json_data=connection_target_dict)
    c.sinks.append(Target(json_data=connection_target_dict))
    c.sinks.append(Target(json_data=connection_target_dict))
    c.paths.append(
        ConnectionPath.from_parchmint_v1_2(
            json_data=connection_path_dict, device_ref=device
        )
    )
    c.paths.append(
        ConnectionPath.from_parchmint_v1_2(
            json_data=connection_path_dict, device_ref=device
        )
    )
    c.layer = layer
    c.entity = "CHANNEL"
    c.params = Params(json_data=params_dict)
    assert c.to_parchmint_v1_2() == connection_dict


def test_connection_from_parchmint_v1_2(
    connection_dict, layer_dict, feature_dict, device
):
    feat = Feature.from_parchmint_v1_2(json_data=feature_dict, device_ref=device)
    device.add_feature(feat)
    c = Connection.from_parchmint_v1_2(json_data=connection_dict, device_ref=device)
    assert c.to_parchmint_v1_2() == connection_dict
