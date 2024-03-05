from app.FileBaseActions import FileBaseActions
import csv

class FileCsvActions(FileBaseActions):
    """CSV File specific actions"""
    
    
    def readFromFile(self, path: str) -> list:
        """Reads a csv file and returns a list where every row is a dict in the returned list"""
        result = []

        file = open(path, "r")
        content = csv.DictReader(file)
        for row in content:
            result.append(row)
        file.close()

        return result







