from __future__ import annotations
from parchmint.layer import Layer

from typing import Optional
from parchmint.params import Params
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from parchmint.device import Device


class Feature:
    """Feature represent atomic manufacturing artifacts"""

    def __init__(
        self,
        id: Optional[str] = None,
        feature_type: Optional[str] = None,
        macro: Optional[str] = None,
        params: Optional[Params] = None,
        layer: Optional[Layer] = None,
        json_data=None,
        device_ref: Device = None,
    ) -> None:
        """Constructor for the feature class

        Args:
            id (Optional[str], optional): id of the feature. Defaults to None.
            feature_type (Optional[str], optional): feature type(geometric operation). Defaults to None.
            macro (Optional[str], optional): unique key indicating the drawing algorithm. Defaults to None.
            params (Optional[Params], optional): geometric parameters for the feature. Defaults to None.
            layer (Optional[Layer], optional): layer in which the feature is in. Defaults to None.
            json_data ([type], optional): loads the data from json. Defaults to None.
            device_ref (Device, optional): pointer to the device object. Defaults to None.

        Raises:
            ValueError: Raises an error if the device pointer isn't there during the json loading process
        """
        self._id = id
        self._type = feature_type
        self._macro = macro
        self._params = params
        self._layer = layer

        if json_data is not None:
            if device_ref is not None:
                self.from_parchmint_v1_x(json_data, device_ref)
            else:
                raise ValueError("device_ref is required")

    @property
    def ID(self) -> str:
        """ Returns the ID of the features"""
        if self._id is None:
            raise ValueError("ID is not set")
        return self._id

    @ID.setter
    def ID(self, value: str) -> None:
        """ Sets the ID of the features"""
        self._id = value

    @property
    def type(self) -> str:
        """ Returns the type of the features"""
        if self._type is not None:
            return self._type
        else:
            raise ValueError("Feature type is not set")

    @type.setter
    def type(self, value: str) -> None:
        """ Sets the type of the features"""
        self._type = value

    @property
    def macro(self) -> str:
        """ Returns the macro of the features"""
        if self._macro is not None:
            return self._macro
        else:
            raise Exception("Macro is not set")

    @macro.setter
    def macro(self, value: str) -> None:
        """ Sets the macro of the features"""
        self._macro = value

    @property
    def params(self) -> Params:
        """ Returns the params of the features"""
        if self._params is not None:
            return self._params
        else:
            raise Exception("No params set")

    @params.setter
    def params(self, value: Params) -> None:
        """ Sets the params of the features"""
        self._params = value

    def to_parchmint_v1_x(self):
        """
        Returns a dict that can be converted to a json string
        """
        return {
            "id": self.ID,
            "type": self.type,
            "macro": self.macro,
            "params": self.params.to_parchmint_v1(),
            "layerID": self._layer.ID if self._layer is not None else None,
        }

    def from_parchmint_v1_x(self, json_data, device_ref: Device) -> None:
        """
        Parses the JSON data of feature
        """
        self.ID = json_data["id"]
        self.type = json_data["type"]
        self.macro = json_data["macro"]
        self.params = Params(json_data=json_data["params"])
        self._layer = device_ref.get_layer(json_data["layerID"])