from app.FileBaseActions import FileBaseActions

class FileTxtActions(FileBaseActions):
    """Txt file specific actions. This is very specific to this project, at this point is not really generic"""
    
    
    def readFromFile(self, path: str) -> list:
        """Reads the txt file specific to this project and returns each line in a list, where each line is a dict. The header is hardcoded"""
        result = []
        file = open(path, "r")
        content = file.read()

        for row in content.split("\n"):
            data = {}
            items = row.split(",")
            try:
                data["IdPersoana"] = items[0].strip()
                data["Data"] = items[1].strip()
                data["Sens"] = items[2].replace(";", "").strip()
            except IndexError:
                continue

            result.append(data)

        file.close()

        return result