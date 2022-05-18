from parchmint import Target


def test_to_parchmint_v1(connection_target_dict):
    target = Target()
    target.component = "c1"
    target.port = "1"
    assert target.to_parchmint_v1() == connection_target_dict

    # Test with load from dict
    target = Target(json_data=connection_target_dict)
    assert target.to_parchmint_v1() == connection_target_dict
