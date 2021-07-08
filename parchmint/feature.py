
from typing import Optional


class Feature:
    """The Feature type object is a representation of the smallest manufacturable 
    artifact.

    Currently we are allowing for feature type to flexible to allow for different types
    of manufacturable features. This will be extended in the future to have fixed types
    of features like "ADD", "SUBTRACT", "UNION" and "INTERSECTION".

    """

    def __init__(self, id:str = None, feature_type:str = None) -> None:
        """This is the feature constructor

        Args:
            id (str, optional): unique ID of the feature. Defaults to None.
            feature_type (str, optional): type of feature for manufacturing. Defaults 
                to None.

        Raises:
            ValueError: [description]
        """
        if id is None:
            raise ValueError()
        
        self._ID:str = id
        self._feature_type:Optional[str] = feature_type

    @property
    def ID(self) -> str:
        return self._ID


class ConnectionFeature:
    """ConnectionFeature type object that enables modifications to the connection
    object, can indicate everything from breaks (for normally closed valves), 
    patterns, tapers, etc. 
    """

    def __init__(self, id: str, feature_type:str, position:float) -> None:
        """Creates a ConnectionFeature type object

        Args:
            id (str): Unique ID of the feature
            feature_type (str): Type of the feature, typically used for manufacturing
            position (float): Position of the feature relative from "source" location
        """
        self._feature = Feature(id=id, feature_type=feature_type)
        self._position = position

    @property
    def ID(self) -> str:
        return self._feature.ID

    @property
    def position(self) -> float:
        """Returns the position of the feature in relative source location along
        the ConnectionPath

        [extended_summary]

        Returns:
            float: [description]
        """
        return self._position
