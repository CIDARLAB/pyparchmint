![Docs Status](https://readthedocs.org/projects/pyparchmint/badge/)

# ParchMINT object library in Python

## About

Microfluidics based laboratory-on-a-chip (LoC) devices have been gaining traction in academia and industry in recent years. These devices are capable of automating biological experiments at mico-liter scale and below. The algorithms for design automation of these devices have been maturing in recent years yet there has been no development of a benchmark suite for use in analyzing the quality of algorithms from different institutions and research groups. We propose here a collection of real life LoC devices that have been specified in a standard notation, along with results from several recent placement and routing algorithms. This suite will enable researchers to quickly validate their algorithms and compare them against the cutting edge from other researchers.

Check [ParchMINT](https://parchmint.org) (https://parchmint.org) for more information on ParchMINT.


### Submitting RCF

Any changes to the parchmint standard need to done by submitting RFC proposals. Proposals will need to be submitted via [Github Issues](https://github.com/CIDARLAB/parchmint/issues) on the ParchMINT Github repository.

### CLI Tools

Once installed in a development environment or in the system environment, the package enables command line tools:

**parchmint-validate**

```
usage: parchmint-validate [-h] input

positional arguments:
  input       This is the file thats used as the input

optional arguments:
  -h, --help  show this help message and exit
```

### Usage in Code

Here's an example of a simple python script that can be used to used to check for errors in a Parchmint JSON.

```
from parchmint import Device
import sys
import json
file_path = sys.argv[1]
print("File Name: " + file_path)
device = None
with open(file_path) as data_file:
    text = data_file.read()
    device_json = json.loads(text)
    device = Device(device_json)
print("Checking for components with no dimensions:")
for component in device.components:
    if component.xspan < 0 or component.yspan < 0:
        print(
            "Component - {} | Type - {} | Dimensions - ({}, {})".format(
                component.ID, component.entity, component.xspan, component.yspan
            )
        )
    for port in component.ports:
        if port.x < 0 or port.y < 0:
            "Component - {} | Type - {} | Port {} - ({}, {})".format(
                component.ID, component.entity, port.label, port.x, port.y
            )
print("Checking for components with no ports:")
for component in device.components:
    if len(component.ports) == 0:
        print("Component - {} | Type - {}".format(component.ID, component.entity))

```


## Installation

### From pypi


```
pip install parchmint
```

### From Source

Clone this repository

```
git clone https://github.com/CIDARLAB/pyparchmint
```

Go to the cloned directory and use poetry to install dependencies

```
poetry install 
```

Installl it into the development environment
```
pip install .
```

### Add as a development dependency


**pip**

```
pip install -e /path/to/parchmint/repository
```

**poetry**

Add the following line into the `pyproject.toml` -> `[tool.poetry.dev-dependencies]` section:

```
[tool.poetry.dev-dependencies]

...

parchmint = {path = "/home/krishna/CIDAR/pyparchmint", develop=true}

```

## License 

BSD 3-Clause License

Copyright (c) 2021, CIDAR LAB
All rights reserved.
