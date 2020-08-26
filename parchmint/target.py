class Target:

    def __init__(self, json=None):
        self.component = None
        self.port = None

        if json:
            self.parse_from_json(json)

    def parse_from_json(self, json):
        self.component = json["component"]
        self.port = json["port"]

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def to_parchmint_v1(self):
        return {
            "component": self.component,
            "port": self.port,
        }