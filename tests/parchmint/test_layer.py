from parchmint import Layer, Params


def test_to_parchmint_v1(params_dict, layer_dict):
    layer = Layer()
    layer.ID = "FLOW_1"
    layer.name = "flow_1"
    layer.type = "FLOW"
    layer.group = ""
    layer.params = Params(params_dict)
    assert layer.to_parchmint_v1() == layer_dict

    # Test to see if the loading from dictionary is working correctly
    layer = Layer(json_data=layer_dict)
    assert layer.to_parchmint_v1() == layer_dict
