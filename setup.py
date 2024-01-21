import os
import mysql.connector as mc
import json

# TODO: Move the functions related to database to the database actions class, the file related functions to the other one.. Maybe...
# TODO: check if the mysql.connector package exists, download it and import it if it doesn't. Nah bro, this is handled by the requirements page. It would be better to do another type of check


"""Use this file to set up everything. Databases, Folders, whatever it is needed.
If there are already things present, they will be deleted and replaced.
The setup.py reset will reset everythingh to the initial states, by removing all the data and dropping the database."""


def readFromJson(path: str) -> dict:
    #TODO: add error handling!
    file = open(path, "r")
    data = json.load(file)
    file.close()
    return data


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
    # We run this only once, we want to stop for good in case of any error.
    data["db"]["host"] = input(f"Database host(Leave it blank to use the default {data['db']['host']}): ")
    data["db"]["user"] = input(f"Database user(Leave it blank if the user is the default {data['db']['user']}): ")
    data["db"]["password"] = input("Database password: ")
    data["db"]["database"] = input(f"Schema(Leave it blank if the default {data['db']['database']} is good enough): ")
    try:
        conn = mc.connect(host=data["db"]["host"], user=data["db"]["user"], password=data["db"]["password"])
        c = conn.cursor()
        conn.close()
    except mc.Error as err:
        print(f"Yeah...No. We need a REAL database. Here's what's wrong:\n{err}")
        exit()
    for folder in data["folders"]:
        folder["path"] = input(f"Where to save the {folder["nice name"]} folder? hit enter if you want to save in the current directory under Data folder: ")
    print(120 * "=")
    # TODO: check if the folder already exists. do nothing otherwise
    writeToJson("res/setupdata.json", data, True)
    return data


def validateUserInfo(userInfo: dict) -> bool:
    """This takes a dictionary of known structure and checks if all the data is valid. Gives errors if something fails, returns true otherwise"""
    return True


def replaceBlankWithDefault(inputValue, defaultValue) -> str:
    return defaultValue


# Database
def createDatabase(dbHost: str, dbUser: str, dbPass: str, dbSchema: str) -> None:
    conn = mc.connect(host=dbHost, user=dbUser, password=dbPass)
    c = conn.cursor()
    c.execute(f"CREATE SCHEMA IF NOT EXISTS `{dbSchema}`; ")
    conn.commit()
    print("Database has been created!")


def createTable(dbHost: str, dbUser: str, dbPass: str, dbSchema: str, table: str, columns: dict):
    conn = mc.connect(host=dbHost, user=dbUser, password=dbPass, database=dbSchema)
    c = conn.cursor()
    queryData = ""
    for key, value in columns.items():
        queryData = f"{queryData}`{key}` {value} NULL, "

    c.execute(f"CREATE TABLE IF NOT EXISTS `{table}` (`Id` INT UNSIGNED NOT NULL AUTO_INCREMENT, {queryData}PRIMARY KEY (`Id`));")
    conn.commit()
    
    print(f"{table} exists from now on")


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
    providedData = getInfoFromUserTerminal()

    db_constants = composeSettings(providedData["db"], "#Database info\n")
    folder_constants = composeSettings(providedData["folders"], "#Data folders\n")

    createDatabase(providedData["db"]["host"], providedData["db"]["user"], providedData["db"]["password"], providedData["db"]["database"])
    for table in providedData["tables"]:
        createTable(providedData["db"]["host"], providedData["db"]["user"], providedData["db"]["password"], providedData["db"]["database"], table["name"], table["columns"])
    for folder in providedData["folders"]:
        os.makedirs(folder["path"])
    writeToFile("constants.py", f"{db_constants}\n{folder_constants}")


# Finally, run the damned thing
setup()

