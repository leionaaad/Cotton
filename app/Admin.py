import datetime
import smtplib
from email.mime.multipart import MIMEMultipart as mmp
from email.mime.text import MIMEText as mt

class Admin:
    """Administrative tasks, like calculating times and sending files and emails"""

    def __init__(self, mailserver: str, mailuser: str, mailpass: str, mailport: int) -> None:
        self.mailserver = mailserver
        self.mailuser = mailuser
        self.mailpassword = mailpass
        self.mailport = mailport


    def calculateTime(self, data: list) -> float:
        """Calculate the time based of a list of entries of known structure. It returns a dict, where the ID is the key, the time is expressed in seconds"""
        hours = {}

        # build a set, so we can see how many guys are there
        uniques = set()
        for item in data:
            uniques.add(item[0])

        # now by each member of the set loop through the entire list and calculate intervals
        for member in uniques:
            start = None
            end = None
            for item in reversed(data):
                if item[0] == member:
                    if item[-1] == "out":
                        end = item[1]
                    elif item[-1] == "in":
                        start = item[1]
                    if not start == None and not end == None: 
                        timediff = end - start
                        if not str(member) in hours.keys():
                            hours[str(member)] = timediff.total_seconds()
                        else:
                            hours[str(member)] += timediff.total_seconds()
                        start = None
                        end = None

        return hours
    

    def sendEmail(self, recipient: str, subject: str, content: str):
        """sends an email using gmail service. it has the following parameters: sender, recipient, subject, content. All strings, all self-evident"""
        message = mmp()
        message["From"] = self.mailuser
        message["To"] = recipient
        message["Subject"] = subject
        
        message.attach(mt(content, "plain"))

        server = smtplib.SMTP_SSL(self.mailserver, self.mailport)
        server.login(self.mailuser, self.mailpassword)
        server.sendmail(self.mailuser, recipient, message.as_string())

        server.quit()



