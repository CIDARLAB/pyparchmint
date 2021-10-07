import glob
import subprocess
import sys
from pathlib import Path

from parchmint.device import Device


def test():
    """
    Run all unittests. Equivalent to:
    `poetry run python -u -m unittest discover`
    """
    subprocess.run(["pytest", "-vv"])


def validate_dir_V1():
    # glob through all the files in the argv directory with .json extension
    files = glob.glob("{}/**/*.json".format(sys.argv[1]), recursive=True)
    for file in files:
        print(file)
        file_path = Path(file).resolve()
        with open(file_path) as data_file:
            Device.validate_V1(data_file.read())


def validate_dir_V1_2():
    # glob through all the files in the argv directory with .json extension
    files = glob.glob("{}/**/*.json".format(sys.argv[1]), recursive=True)
    for file in files:
        print(file)
        file_path = Path(file).resolve()
        with open(file_path) as data_file:
            Device.validate_V1(data_file.read())
