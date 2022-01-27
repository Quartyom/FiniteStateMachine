import json

class Qu_json:

    def __init__(self, file_path):
        self.data = dict()
        self.file_path = file_path

        try: self.load()
        except: self.save()

    def save(self):
        with open(self.file_path, "w") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
            return self.data
            
    def load(self):
        with open(self.file_path, "r") as file:
            self.data = json.load(file)
            return self.data

