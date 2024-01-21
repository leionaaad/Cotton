import os
import mysql.connector as mc
import json


def deleteDatabase(dbHost: str, dbUser: str, dbPass: str, dbSchema: str) -> None:
    conn = mc.connect(host=dbHost, user=dbUser, password=dbPass)
    c = conn.cursor()
    c.execute(f"DROP SCHEMA `COTTON`")
    conn.commit()


def unsetup() -> None:
    # delete the database
    # delete the data folders
    # delete the config files
    # this will not remove the downloaded packages!
    # confirm if the database needs to be removed or left alone
    #get the data from the json
    os.rename("res/setupdata.json.bak", "res/setupdata.json")
    deleteDatabase(host, user, password, database)
    print("Done! You're back to step 1.")
    os.remove("res/setupdata.json")     #TODO: do't touch it, if it doesn't have a backup!
    os.remove("constants.py")


unsetup()

#TODO: have an option to remove all the data and database too.