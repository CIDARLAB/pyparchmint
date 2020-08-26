class Params:

    def __init__(self, json=None):

        self.data = dict()

        if json:
            self.parse_from_json(json)

    def get_param(self, key):
        return self.data[key]

    def set_param(self, key: str, value):
        self.data[key] = value

    def exists(self, key):
        return key in self.data.keys()

    def parse_from_json(self, json):

        for key, value in json.items():
            self.data[key] = value

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def to_parchmint_v1(self):
        return self.data
