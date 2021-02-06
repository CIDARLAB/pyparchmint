class Params:
    def __init__(self, json=None):
        """Creates an instance of the params

        Args:
            json (dict, optional): json dict form json.loads(). Defaults to None.
        """
        self.data = dict()

        if json:
            self.parse_from_json(json)

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
