from parchmint import Params


def test_params_to_parchmint_v1_x_dict(params_dict):
    params = Params()
    params.set_param("channelWidth", 1000)
    params.set_param("rotation", 25)
    params.set_param("position", [250, 300])
    params.set_param("direction", "UP")
    parchmint_dict = params.to_parchmint_v1()
    assert parchmint_dict == params_dict

    # Test to see if the loading from dictionary is working correctly
    params = Params(params_dict)
    assert params.to_parchmint_v1() == params_dict
