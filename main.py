# TODO: Somewhere add a mapping, so csv headers and db columns can be matched.

import sys, time
from flask import Flask, request
from app.GateBase import GateBase as gb
try:
    from constants import *
except ModuleNotFoundError:
    print("Constants.py is missing. It's either not set up properly, either some moron messed with the files.\nRun setup.py to set everything up, only then run main.py")
    exit()


args = sys.argv
tick = 2
timecutoff = 20

#Temporary!
args = ["main.py", "2"]

gateActions = gb(host, user, password, database, "access")


def main():
    while True:
        gateActions.uploadDataFromFolder(entries, entries_backup)
        print(f"watching {entries} for changes")
        time.sleep(tick)


# Flask Server

app = Flask(__name__)

@app.route("/")
def hello():
    return "Motherfucker"

@app.route("/admin", methods = ["GET"])
def showAdminPage():
    return "this is the admin page, buddy"

@app.route("/admin", methods = ["POST"])
def getAdminData():
    return f"some admin data has been received {request.json}"


@app.route("/gate", methods = ["POST"])
def gateEntry():
    gateActions.uploadDataFromEndpoint(request.json)
    return "Gate usage logged."


# Run the goddamned thing
if args[1] == "1":
    main()

elif args[1] == "2":
    if __name__ == "__main__":
        app.run(host, 5000, True)

elif args[1] == "3":
    print("Not implemented yet, move along")
    exit()




