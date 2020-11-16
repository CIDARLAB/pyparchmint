from parchmint.device import Device


def validate_V1(file_path):
    with open(file_path) as data_file:
        Device.validate_V1(data_file.read())