import os
import shutil
import mysql.connector as mc
import json
from app.DbBaseActions import DbBaseActions as dba


# this is only temporary, Until I make the file I/O classes
def getDataFromJson(pathToJson) -> dict:
    file = open(pathToJson, "r")
    result = json.load(file)
    file.close()
    return result


def unsetup(deleteDb: bool, deleteFolders: bool) -> None:
    #TODO: check if constants.py exists. Assume nothing to do if it doesn't
    setupdata = getDataFromJson("res/setupdata.json")
    if deleteDb:
        dbase = dba(setupdata["db"]["host"], setupdata["db"]["user"], setupdata["db"]["password"], setupdata["db"]["database"])
        dbase.deleteDatabase()
    if deleteFolders:
        for folder in setupdata["folders"]:
            #TODO: check the empty parent folder.
            shutil.rmtree(folder["path"])

    os.remove("res/setupdata.json")     #TODO: do't touch it, if it doesn't have a backup!
    os.rename("res/setupdata.json.bak", "res/setupdata.json")
    os.remove("constants.py")
    print("Done! You're back to step 1.")


unsetup(True, True)