# TODO: Somewhere add a mapping, so csv headers and db columns can be matched.

import os
import time
from flask import Flask
from app.GateBase import GateBase as gb
try:
    from constants import *
except ModuleNotFoundError:
    print("Constants.py is missing. It's either not set up properly, either some moron messed with the files.\nRun setup.py to set everything up, only then run main.py")


tick = 2
timecutoff = 20

gateActions = gb(host, user, password, database, "access")


time.sleep(tick)

def main():
    while True:
        time.sleep(tick)
        gateActions.uploadDataFromFolder(entries, entries_backup)

main()







