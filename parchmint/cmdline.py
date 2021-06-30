import argparse
from pathlib import Path

from parchmint.device import Device


def validate_V1():
    parser = argparse.ArgumentParser()

    parser.add_argument("input", help="This is the file thats used as the input ")

    args = parser.parse_args()
    file_path = Path(args.input).resolve()
    with open(file_path) as data_file:
        Device.validate_V1(data_file.read())
