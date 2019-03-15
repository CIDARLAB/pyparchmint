class Params:

    def __init__(self, json):

        self.data = dict()

        if json:
            self.parseFromJSON(json)


    def parseFromJSON(self, json):

        for key, value in json.items():
            self.data[key] = value

    def __str__(self):
            return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)
