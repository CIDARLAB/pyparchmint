class Params:

    def __init__(self, json=None):

        self.data = dict()

        if json:
            self.parseFromJSON(json)

    def getParam(self, key):
        return self.data[key]

    def setParam(self, key:str, value):
        self.data[key] = value

    def exists(self, key):
        return key in self.data.keys()

    def parseFromJSON(self, json):

        for key, value in json.items():
            self.data[key] = value

    def __str__(self):
            return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def toParchMintV1(self):
        return self.data
    
