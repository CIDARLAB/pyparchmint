from .params import Params


class Component:

    def __init__(self, json=None):
        self.name = None
        self.ID = None
        self.params = dict()
        self.entity = None
        self.xpos = None
        self.ypos = None
        self.xspan = None
        self.yspan = None

        if json:
            self.parseFromJSON(json)


    def parseFromJSON(self, json):
        self.name = json["name"]
        self.ID = json["id"]
        self.entity = json["entity"]
        self.xspan = json["xspan"]
        self.yspan = json["yspan"]
        self.params = Params(json["params"])
        
        if self.params:
            self.xpos = self.params.getParam("position")[0]
            self.ypos = self.params.getParam("position")[1]

    def __str__(self):
            return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)