from app.FileBaseActions import FileBaseActions
import csv

class FileCsvActions(FileBaseActions):
    """CSV File specific actions"""
    
    
    def readFromFile(self, path: str) -> list:
        """Reads a csv file and returns a list where every row is a dict in the returned list. It also uses the file name to get the gate index"""
        result = []
        infoFromName = self.interpretFilename(path)

        file = open(path, "r")
        content = csv.DictReader(file)
        for row in content:
            row["Poarta"] = infoFromName["index"]
            result.append(row)
        file.close()

        return result
    
    def writeListToFile(self, path: str, content: list, overwrite: bool = True) -> None:
        """Writes a list of same structure dictionaryies to a file"""
        csvfile = open(path, "w", newline="")
        writer = csv.DictWriter(csvfile, fieldnames=content[0].keys())
        writer.writeheader()
        for row in content:
            writer.writerow(row)
        csvfile.close()





