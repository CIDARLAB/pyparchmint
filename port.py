class Port:

    def __init__(self, json=None):
        self.x = None
        self.y = None
        self.label = None
        self.layer = None

        if json:
            self.parseFromJSON(json)
    
    def parseFromJSON(self, json):
        self.x = json["x"]
        self.y = json["y"]
        self.label = json["label"]
        self.layer = json["layer"]

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def toParchMintV1(self):
        data = {}

        data["x"] = self.x
        data["y"] = self.y
        data["label"] = self.label
        data["layer"] = self.layer
        
        return data
