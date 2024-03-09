from app.DbAccessActions import DbAccessActions as dba
from app.FileBaseActions import FileBaseActions as fba
from app.FileCsvActions import FileCsvActions as csva
from app.FileTxtActions import FileTxtActions as txta
from datetime import datetime
import os

# TODO: Table name is hardcoded. use either constants, or the setupdata json

class GateBase:
    """Base class for all the possible gates. It contains the common methods: upload to the database"""

    def __init__(self, dbhost, dbuser, dbpassword, dbschema, table) -> None:
        self.dbActions = dba(dbhost, dbuser, dbpassword, dbschema, table)
        self.fileActions = fba()


    def uploadDataFromFolder(self, entriesPath, backupPath) -> None:
        """Reads a folder for txt and cvs files and uploads the data to the database. After that, the files are moved to the backup. It has two parameters: entriesPath for the entries folder, backupPath for the backup folder"""

        txtActions = txta()
        csvActions = csva()
        tstamp = str(int(datetime.now().timestamp()))
        print(len(os.listdir(entriesPath)))
        if len(os.listdir(entriesPath)) > 0:
            os.mkdir(f"{backupPath}/{tstamp}")

        for file in os.listdir(entriesPath):
            if self.fileActions.interpretFilename(file)["extension"] == "txt":
                for row in txtActions.readFromFile(f"{entriesPath}/{file}"):
                    self.dbActions.addEntry(row)
            elif self.fileActions.interpretFilename(file)["extension"] == "csv":
                for row in csvActions.readFromFile(f"{entriesPath}/{file}"):
                    self.dbActions.addEntry(row)
            self.fileActions.filebackup(f"{entriesPath}/{file}", f"{backupPath}/{tstamp}/{file}", True)

    def uploadDataFromEndpoint(self, jsondata):
        """takes a provided dict of known structure and uploads it to a database."""
        self.dbActions.addEntry(jsondata)



