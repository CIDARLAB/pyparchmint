from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional

from parchmint.layer import Layer
from parchmint.params import Params

if TYPE_CHECKING:
    from parchmint.device import Device


class Feature:
    """Feature represent atomic manufacturing artifacts"""

    def __init__(
        self,
        feature_id: Optional[str] = None,
        feature_type: Optional[str] = None,
        macro: Optional[str] = None,
        params: Optional[Params] = None,
        layer: Optional[Layer] = None,
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
        self._id = feature_id
        self._type = feature_type
        self._macro = macro
        self._params = params
        self._layer = layer

    @property
    def ID(self) -> str:
        """Returns the ID of the features"""
        if self._id is None:
            raise ValueError("ID is not set")
        return self._id

    @ID.setter
    def ID(self, value: str) -> None:
        """Sets the ID of the features"""
        self._id = value

    @property
    def type(self) -> str:
        """Returns the type of the features"""
        if self._type is not None:
            return self._type
        else:
            raise ValueError("Feature type is not set")

    @type.setter
    def type(self, value: str) -> None:
        """Sets the type of the features"""
        self._type = value

    @property
    def macro(self) -> str:
        """Returns the macro of the features"""
        if self._macro is not None:
            return self._macro
        else:
            raise Exception("Macro is not set")

    @macro.setter
    def macro(self, value: str) -> None:
        """Sets the macro of the features"""
        self._macro = value

    @property
    def params(self) -> Params:
        """Returns the params of the features"""
        if self._params is not None:
            return self._params
        else:
            raise Exception("No params set")

    @params.setter
    def params(self, value: Params) -> None:
        """Sets the params of the features"""
        self._params = value

    def to_parchmint_v1_2(self):
        """
        Returns a dict that can be converted to a json string
        """
        return {
            "id": self._id,
            "type": self.type,
            "macro": self.macro,
            "params": self.params.to_parchmint_v1(),
            "layerID": self._layer.ID if self._layer is not None else None,
        }

    @staticmethod
    def from_parchmint_v1_2(json_data: Dict, device_ref: Device) -> Feature:
        """
        Parses the JSON data of feature
        """
        feature = Feature(
            feature_id=json_data["id"],
            feature_type=json_data["type"],
            macro=json_data["macro"],
            params=Params(json_data=json_data["params"]),
            layer=device_ref.get_layer(json_data["layerID"]),
        )
        return feature
