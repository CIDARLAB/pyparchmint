class Target:

    def __init__(self, json):
        self.component = None
        self.port = None

        if json:
            self.parseFromJSON(json)

    
    def parseFromJSON(self, json):
        self.component = json["component"]
        self.port = json["port"]


    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)
