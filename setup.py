import os
from app.DbBaseActions import DbBaseActions as dba
from app.FileBaseActions import FileBaseActions as fba
from app.FileJsonActions import FileJsonActions as jsa


"""Use this file to set up everything. Databases, Folders, whatever it is needed.
If there are already things present, they will be deleted and replaced.
The setup.py reset will reset everythingh to the initial states, by removing all the data and dropping the database."""


# get the needed information from the user
def getInfoFromUserTerminal() -> dict :
    """Collects the data from the user and returns it as a dictionary of known structure."""

    jsonActions = jsa()
    fileActions = fba()
    data = jsonActions.readFromFile("res/setupdata.json")
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
    fileActions.filebackup("res/setupdata.json", "res/setupdata.json.bak", False)
    jsonActions.writeToFile("res/setupdata.json", data, True)
    # writeToJson("res/setupdata.json", data, True)
    return data


def setup(providedData: dict) -> None :
    """Uses data from the dictionary provided to set up the database, the folders, the everything."""
    if os.path.exists("constants.py"):
        print("Seems like this is already set up, buddy")
        exit()

    dbase = dba(providedData["db"]["host"], providedData["db"]["user"], providedData["db"]["password"])
    fileActions = fba()

    db_constants = fileActions.composeSettings(providedData["db"], "#Database info\n")
    folder_constants = fileActions.composeSettings(providedData["folders"], "#Data folders\n")

    dbase.createDatabase(providedData["db"]["database"], True)

    for table in providedData["tables"]:
        dbase.createTable(table, False)

    for folder in providedData["folders"]:
        os.makedirs(folder["path"])
    fileActions.writeToFile("constants.py", f"{db_constants}\n{folder_constants}", True)
    print("apparently everything just has been set up properly.")


# Finally, run the damned thing
setup(getInfoFromUserTerminal())

