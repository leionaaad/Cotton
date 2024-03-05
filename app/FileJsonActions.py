from app.FileBaseActions import FileBaseActions
import json


class FileJsonActions(FileBaseActions):
    """Json Specific actions"""
    

    # TODO: add error handling! Maybe the file is not there, or maybe it's not a json
    def readFromFile(self, path: str) -> dict:
        """Reads a joson and returns a dict. Requires only the path as parameter."""
        result = {}
        file = open(path, "r")
        result = json.load(file)
        file.close()
        return result
    

    def writeToFile(self, path: str, content: dict, overwrite: bool = True) -> None:
        """Writes a dictionary to a json. It needs a path, content and there is also an optional bool to overwrite or not. By default it overwrites."""
        file = open(path, "w")
        json.dump(content, file)
        file.close()