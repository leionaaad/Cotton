import os
import mysql.connector as mc
import json
from app.DbBaseActions import DbBaseActions as dba


"""Use this file to set up everything. Databases, Folders, whatever it is needed.
If there are already things present, they will be deleted and replaced.
The setup.py reset will reset everythingh to the initial states, by removing all the data and dropping the database."""

#TODO: This will be handled by a class
def readFromJson(path: str) -> dict:
    #TODO: add error handling!
    file = open(path, "r")
    data = json.load(file)
    file.close()
    return data

#TODO: This will be handled by a class. This is only a temporary function
def writeToJson(path: str, content: dict, backup=False) -> dict:
    #TODO: add error handling. Especially with the backup file.
    if backup == True:
        os.rename(path, f"{path}.bak")
    file = open(path, "w")
    json.dump(content, file)
    file.close()


# get the needed information from the user
def getInfoFromUserTerminal() -> dict :
    data = readFromJson("res/setupdata.json")
    print("\nGood day to you, sir.\n")
    print("The following are goin' to happen:\n\t-You will be asked the db and a connection to a database will be attempted \
          \n\t-If the provided database doesn't exist a new one will be created, otherwise the provided one will be used.\
          \n\t-Files with the settings will be created in this working folder \
          \n\t-Folder for the data will be created in the specified location.\
          \n\t-These settings can be manually changed at a later time in the constants.py file.")
    print(120 * "=")
    host = input(f"Database host(Leave it blank to use the default {data['db']['host']}): ")
    if not host == "":
        data["db"]["host"] = host
    user = input(f"Database user(Leave it blank if the user is the default {data['db']['user']}): ")
    if not user == "":
        data["db"]["user"] = user
    data["db"]["password"] = input("Database password: ")
    database = input(f"Schema(Leave it blank if the default {data['db']['database']} is good enough): ")
    if not database == "":
        data["db"]["database"] = database
    # now we are just testing the connection, the following instance is ok not to be asigned to any variable
    dba(data["db"]["host"], data["db"]["user"], data["db"]["password"])

    for folder in data["folders"]:
        pathToFolder = input(f"Where to save the {folder["nice name"]} folder? hit enter if you want to save in the current directory under Data folder: ")
        if not pathToFolder == "":
            folder["path"] = pathToFolder
    print(120 * "=")
    # TODO: check if the folder already exists. do nothing otherwise
    writeToJson("res/setupdata.json", data, True)
    return data

#TODO: this will be handled by a class
# Folders and files
def writeToFile(pathToFile: str, content: str) -> None :
    # TODO: check if file already exists, 
    file = open(pathToFile, "w")
    file.write(content)
    file.close()
    print(f"{pathToFile} is ready.")


def composeSettings(source: dict, head="", tail="") -> str:
    fileVars = head
    if type(source) == dict:
        for key, value in source.items():
            fileVars = f"{fileVars}{key} = \"{value}\"\n"
    elif type(source) == list:
        for item in source:
            fileVars = f"{fileVars}{item["name"]} = \"{item["path"]}\"\n"
    return fileVars


def setup() -> None :
    #TODO: check if constants already exists. If it does, assume it was already installed
    providedData = getInfoFromUserTerminal()
    dbase = dba(providedData["db"]["host"], providedData["db"]["user"], providedData["db"]["password"])

    db_constants = composeSettings(providedData["db"], "#Database info\n")
    folder_constants = composeSettings(providedData["folders"], "#Data folders\n")

    dbase.createDatabase(providedData["db"]["database"], True)

    for table in providedData["tables"]:
        dbase.createTable(table, False)

    for folder in providedData["folders"]:
        os.makedirs(folder["path"])
    writeToFile("constants.py", f"{db_constants}\n{folder_constants}")


# Finally, run the damned thing
setup()

