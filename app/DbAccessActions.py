from app.DbBaseActions import DbBaseActions
from datetime import datetime as dt


class DbAccessActions(DbBaseActions):
    """This is a convenient way to insert entries in the Access table of the database."""

    def __init__(self, host: str, user: str, password: str, database: str, table: str) -> None:
        super().__init__(host, user, password, database)
        self.table = table
        self.__conn = self.getConn()
        self.__cursor = self.getCursor()


    def addEntry(self, data: dict) -> None:
        """Yes, this exists in the parent class, but here uses a specific, more conveniant way to insert data into the access table. Basically a shorter way of doing things."""
        # TODO: correct the timestamp!
        timestamp = dt.strptime(data["Data"], "%Y-%m-%dT%H:%M:%S.%fZ")
        dbTimestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        self.__cursor.execute(f"INSERT INTO `{self.table}` VALUES (Null, \"{data['IdPersoana']}\", \"{dbTimestamp}\", \"{data['Sens']}\", \"{data['Poarta']}\"); ")
        self.__conn.commit()


    def getDailyEntries(self, date: str) -> tuple:
        """Provide a date in the format YYYY-mm-dd ant get all the enries of that specific date"""
        self.__cursor.execute(f"SELECT IdPersoana, Data, Sens FROM `{self.table}` WHERE DATE(Data) = \"{date}\"")
        result = self.__cursor.fetchall()
        return result
