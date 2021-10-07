from parchmint import Params
from parchmint.feature import Feature
from parchmint.layer import Layer


def test_to_parchmint_v1(feature_dict, params_dict, device, layer):
    feat = Feature(
        id="feat1",
        feature_type="UNION",
        macro="TYPE1",
        params=Params(json_data=params_dict),
        layer=layer,
        device_ref=device,
    )

    assert feat.to_parchmint_v1_x() == feature_dict


def test_from_parchmint_v1_x(feature_dict, device):

    feat = Feature(json_data=feature_dict, device_ref=device)
    assert feat.to_parchmint_v1_x() == feature_dict
