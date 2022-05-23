import argparse
from pathlib import Path

from parchmint.device import Device


def validate_v1():
    """Validate the json file against the schema v1"""

    parser = argparse.ArgumentParser()

    parser.add_argument("input", help="This is the file thats used as the input ")

    args = parser.parse_args()
    file_path = Path(args.input).resolve()
    with open(file_path, encoding="utf-8") as data_file:
        Device.validate_v1(data_file.read())
