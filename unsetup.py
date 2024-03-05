import os
import shutil
import mysql.connector as mc
from app.DbBaseActions import DbBaseActions as dba
from app.FileJsonActions import FileJsonActions as jsa


"""This will remove everything. Settings files, database tables, everything and will start from zero."""


def unsetup(deleteDb: bool, deleteFolders: bool) -> None:
    if not os.path.exists("constants.py"):
        print("Nothing to do, looks like nothing is set up yet.")
        exit()

    jsonActions =  jsa()
    setupdata = jsonActions.readFromFile("res/setupdata.json")
    
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


# TODO: Make this an interactive thing too.
unsetup(True, True)