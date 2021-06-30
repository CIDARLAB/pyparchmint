from os import truncate


class Params:
    def __init__(self, json=None):
        """Creates an instance of the params

        Args:
            json (dict, optional): json dict form json.loads(). Defaults to None.
        """
        self.data = {}

        if json:
            self.parse_from_json(json)

    def __ne__(self, other) -> bool:
        """operator overload to compare two params.
        ex. P1 != P2

        Args:
            other (Params): P2 part

        Returns:
            bool: Return true if NOT equal. Otherwise false
        """
        len1 = len(self.data)
        len2 = len(self.data)

        if len1 != len2:
            return True
        else:
            for item in self.data:
                if item not in other.data:
                    return True
                else:
                    if self.data[item] != other.data[item]:
                        return True

        return False

    def get_param(self, key: str):
        """Returns the value stored against the key

        Args:
            key (str): parameter name

        Returns:
            [type]: [description]
        """
        return self.data[key]

    def set_param(self, key: str, value):
        """Sets the value for a given key to the param

        Args:
            key (str): parameter name
            value (): value to be stored against the key
        """
        self.data[key] = value

    def exists(self, key: str) -> bool:
        """Checks if the key exists in the params

        Args:
            key (str): key of the param

        Returns:
            bool: true if key is present in the params
        """
        return key in self.data.keys()

    def parse_from_json(self, json):
        """Parses from the json dict

        Args:
            json (dict): json dict after json.loads()
        """
        for key, value in json.items():
            self.data[key] = value

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def to_parchmint_v1(self) -> dict:
        """Returns the json dict

        Returns:
            dict: dictionary that can be used in json.dumps()
        """
        return self.data
