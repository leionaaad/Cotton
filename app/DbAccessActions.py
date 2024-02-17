from app.DbBaseActions import DbBaseActions
import mysql.connector as mc

class DbAccessActions(DbBaseActions):
    def __init__(self, host: str, user: str, password: str, database: str = None, table: str = None) -> None:
        super().__init__(host, user, password, database)
        self.table = table

    def addEntry(self, data: dict) -> None:
        """Yes, this exists in the parent class, but here uses a specific, more conveniant way to insert data into the access table. Basically a shorter way of doing things."""
        self.__cursor.execute(f"INSERT INTO `{self.table}` VALUES (Null, '{data["person"]}', '{data["date"]}', '{data["direction"]}', '{data["gate"]}'); ")
        self.__conn.commit()

