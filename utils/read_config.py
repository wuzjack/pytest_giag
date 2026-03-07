import json


class ReadConfig:
    def __init__(self,filename):
        self.filepath = filename

        with open(self.filepath,"r",encoding="utf-8") as f:
            self.data = json.load(f)

    def getValue(self,section,name):
        return self.data.get(section,{}).get(name)