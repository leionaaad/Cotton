# Setting things up - DONE
# -venv - DONE
# -gitignore - DONE
# -Known required folders - DONE
# - requirements.txt - NOT DONE
# - check if everything is set up - NOT DONE
# unsetup - DONE

from app.DbAccessActions import DbAccessActions as dbaa
from app.DbPersonalActions import DbPersonalActions as dbpa
from app.FileCsvActions import FileCsvActions as csva
from app.FileTxtActions import FileTxtActions as txta
from app.FileJsonActions import FileJsonActions as jsa
# from constants import *

# Run here the database test code (temporary)


# dba = dbaa("localhost", "root", "anyadkinnya", "cotton", "access")
# dbp = dbpa("localhost", "root", "anyadkinnya", "cotton", "persoane")
# print(dba.table)
# print(dbp.table)

print("CSV ACTIONS")
csvActions = csva()
print(csvActions.readFromFile("E:/Courses/ItSchool/Cotton/doq/Poarta2.csv"))

print("TXT ACTIONS")
txtActions = txta()
print(txtActions.readFromFile("E:/Courses/ItSchool/Cotton/doq/Poarta1.txt"))

print("JSON ACTIONS")
jsonActions = jsa()
print(jsonActions.readFromFile("E:/Courses/ItSchool/Cotton/res/setupdata.json"))
