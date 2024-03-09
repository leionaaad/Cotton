import os
import shutil

class FileBaseActions:
    """Base class for file handling. Generic read, write and navigation"""
    

    def filebackup(self, srcPath: str, destPath: str, deleteOriginal:bool = True) -> None:
        """Copies a file to another location. It has 3 parameters: source, destination (these are full paths to the file), and an optional bool to delete the source, or not. This is set by default to True."""
        # TODO: error handling if file doesn't exist, or if the destination file already exists.
        # TODO: add here the intermediate folders if they don't exist
        shutil.copy(srcPath, destPath)
        if deleteOriginal:
            os.remove(srcPath)


    def interpretFilename(self, path: str) -> dict:
        # TODO: This needs a lot of more work, we want to remove bad filenames with multiple ilands of digits or whatnot
        """In case the filename is composed by the assumed pattern, it returns the pieces of the filename as a dict. It needs only a filepath as parameter. The full path will be discarded, and only the filename itself is considered(including the extension)"""
        parts = {}
        #TODO: Error check if file exists or not.
        file = os.path.splitext(os.path.basename(path))
        # Poarta[numar_poarta].[tip_fisier] (de exemplu Poarta1.csv)
        name = ""
        index = ""
        for character in file[0]:
            if character.isalpha():
                name += character
            elif character.isdigit():
                index += character

        parts["name"] = name
        parts["index"] = int(index)
        parts["extension"] = file[1][1:]
        return parts
    

    def composeSettings(self, source: dict, head="", tail="") -> str:
        """Primarily used in the setup, it returns the key-value pairs from a dict as a list of key = value, that can later be used as a python file that has all the variables in one place"""
        fileVars = head
        if type(source) == dict:
            for key, value in source.items():
                fileVars = f"{fileVars}{key} = \"{value}\"\n"
        elif type(source) == list:
            for item in source:
                fileVars = f"{fileVars}{item["name"]} = \"{item["path"]}\"\n"
        return fileVars


    def writeToFile(self, path: str, content: str, overwrite: bool = True) -> None:
        """Writes a generic content to a generic file. Nothing spectacular. It just outputs everything as it is. Parameters are: path to the file, the content, and a bool to overwrite if the file exists or not. This one is optional, by default is set to overwrite."""
        if not overwrite:
            try:
                file = open(path, "w")
                file.write(content)
                file.close()
            except FileExistsError:
                print("file exists already, Aborting at once!")
        else:
            file = open(path, "w")
            file.write(content)
            file.close()


    def readFromFile(self, path:str) -> str:
        """Reads generic content from a generic ascii file. It only requires a path to the file as parameter."""
        try:
            file = open(path, "r")
            result = file.read()
            file.close()
            return result
        except FileNotFoundError:
            print("Check the path. It seems very very wrong")
            return None
        
