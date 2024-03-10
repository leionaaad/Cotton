import sys, time, os, platform
from datetime import datetime, date
from flask import Flask, request, render_template
from app.GateBase import GateBase as gb
from app.Admin import Admin
from app.DbAccessActions import DbAccessActions as dbaa
from app.DbPersonalActions import DbPersonalActions as dbpa
from app.FileCsvActions import FileCsvActions as csva
from app.FileTxtActions import FileTxtActions as txta
try:
    from constants import *
except ModuleNotFoundError:
    print("Constants.py is missing. It's either not set up properly, either some moron messed with the files.\nRun setup.py to set everything up, only then run main.py")
    exit()


args = sys.argv
checkInterval = 2
timecutoff = 20
requiredHours = 8

#Temporary!
args = ["main.py", "2"]

gateActions = gb(host, user, password, database, "access")
dbPersonalActions = dbpa(host, user, password, database, "persoane")
administer = Admin("mail.leionaaad.com", "chiulangii@leionaaad.com", "anyadkinnya", 465)
dbAccessActions = dbaa(host, user, password, database, "access")
dbPersonalActions = dbpa(host, user, password, database, "persoane")


def main():
    emailSent = False
    while True:
        this_moment = datetime.now().hour
        gateActions.uploadDataFromFolder(entries, entries_backup)
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
        print(f"watching {entries} for changes")
        # send the emails only if the time is correct, and only if the email has not been sent yet
        if this_moment == timecutoff and not emailSent:
            reportAwol(date.today().strftime("%Y-%m-%d"))
            emailSent = True
        # Reset the email sent status for the next day
        if this_moment == 0 and emailSent:
            emailSent = False

        time.sleep(checkInterval)


def reportAwol(date):
    guys = administer.calculateTime(dbAccessActions.getDailyEntries(date))
    awols = []
    for guy in guys:
        if guys[guy] / 3600 < timecutoff:
            guydata = dbPersonalActions.lookupById(int(guy))
            managerdata = dbPersonalActions.lookupById(guydata[4])
            awols.append({"name": guydata[2], "surname": guydata[1], "manager_name": f"{managerdata[2]} {managerdata[1]}", "manager_email": managerdata[-1], "hours": str(int(guys[guy] // 3600)).zfill(2), "minutes": str(int(guys[guy] % 3600) // 60).zfill(2)})
    
    messages = {}
    for item in awols:
        content = {}
        if item["manager_name"] not in messages.keys():
            content["email"] = item["manager_email"]
            content["title"] = f"Dearest {item["manager_name"]}"
            content["body"] = f"The following people were not performing their duties faithfully:\n {item["surname"]} {item["name"]}: {item["hours"]}:{item["minutes"]}"
            messages[item["manager_name"]] = content
        else:
            messages[item["manager_name"]]["body"] = f"{messages[item["manager_name"]]["body"]}\n{item["surname"]} {item["name"]}: {item["hours"]}:{item["minutes"]}"

    for item in messages.values():
        administer.sendEmail(item["email"], f"Chiulangii din {date}", f"{item["title"]}\n\n{item["body"]}")
        time.sleep(2)
    
    fileContent =[]
    for item in awols:
        fileContent.append({"Nume": f"{item["name"]} {item["surname"]}", "Ore Lucrate": f"{item["hours"]}:{item["minutes"]}"})

    csvActions = csva()
    csvActions.writeListToFile(f"{entries_backup}/{date}_chiulangii.csv", fileContent, True)
    txtActions = txta()
    txtActions.writeListToFile(f"{entries_backup}/{date}_chiulangii.txt", fileContent, True)



# Flask Server


app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/admin", methods = ["GET"])
def showAdminPage():
    return render_template("index.html")


@app.route("/submitform", methods = ["POST"])
def addNewGuy():
    managerSurname, managerName = request.form["manager"].split(" ")
    manager_id = dbPersonalActions.lookupIdByName(managerName, managerSurname)
    formresult = {"name": request.form["name"], "surname": request.form["surname"], "company": request.form["company"], "managerId": manager_id, "email": request.form["email"]}
    dbPersonalActions.addEntry(formresult)
    return render_template("formSubmitted.html")


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
    reportAwol("2023-05-21")




