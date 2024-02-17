from app.DbBaseActions import DbBaseActions
import mysql.connector as mc

class DbPersonalActions(DbBaseActions):
    def __init__(self, host: str, user: str, password: str, database: str, table: str) -> None:
        super().__init__(host, user, password, database)
        self.table = table
    
    def addEntry(self, data: dict) -> None:
        """Yes, this exists in the parent class, but here uses a specific, more conveniant way to insert data into the personal table. Basically a shorter way of doing things."""
        #TODO: add error handling.
        self.__cursor.execute(f"INSERT INTO `{self.table}` VALUES (Null, '{data["name"]}', '{data["surname"]}', '{data["company"]}', '{data["managerId"]}', '{data["email"]}'); ")
        self.__conn.commit()

    def removeEntry(self, id: int) -> None:
        """Yes, this exists in the parent class, but here uses a specific, more conveniant way to remove data from the personal table. Basically a shorter way of doing things."""
        self.__cursor.execute(f"DELETE FROM `{self.table}` WHERE (`id` = {id})")
        self.__conn.commit()

    def editEntry(self, id: int, data: dict) -> None:
        dictItems = data.items()
        query = ""
        for i in dictItems:
            query += f"`{dictItems[0]}` = '{dictItems[1]}', "
        self.__cursor.execute(f"UPDATE `{self.table}` SET {query[:-1]} WHERE (`id` = {id})")
        self.__conn.commit()

