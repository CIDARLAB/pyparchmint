from parchmint import Params
from parchmint.feature import Feature


def test_to_parchmint_v1(feature_dict, params_dict):
    feat = Feature(
        id="feat1",
        feature_type="UNION",
        macro="TYPE1",
        params=Params(json_data=params_dict),
    )

    assert feat.to_parchmint_v1_x() == feature_dict


def test_from_parchmint_v1_x(feature_dict, params_dict):
    feat = Feature(json_data=feature_dict)
    assert feat.to_parchmint_v1_x() == feature_dict