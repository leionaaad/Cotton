from app.FileBaseActions import FileBaseActions

class FileTxtActions(FileBaseActions):
    """Txt file specific actions. This is very specific to this project, at this point is not really generic"""
    
    
    def readFromFile(self, path: str) -> list:
        """Reads the txt file specific to this project and returns each line in a list, where each line is a dict. The header is hardcoded.  It also uses the file name to get the gate index"""
        result = []
        infoFromName = self.interpretFilename(path)

        file = open(path, "r")
        content = file.read()
        for row in content.split("\n"):
            data = {}
            items = row.split(",")
            try:
                data["IdPersoana"] = items[0].strip()
                data["Data"] = items[1].strip()
                data["Sens"] = items[2].replace(";", "").strip()
                data["Poarta"] = infoFromName["index"]
            except IndexError:
                continue

            result.append(data)

        file.close()

        return result
    

    def writeListToFile(self, path: str, content: list, overwrite: bool = True) -> None:
        """Writes a txt file. It needs a full path to the file, the conent as a dict and a boolean to overwrite the existing file or not."""
        txtFile = open(path, "w")
        for item in content:
            row = ""
            for part in item.values():
                if row == "":
                    row = part
                else:
                    row = f"{row}, {part}"
            txtFile.writelines(f"{row};\n")
        txtFile.close()