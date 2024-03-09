import mysql.connector as mc

class DbBaseActions:
    """The base actions for the database, like connections and all the basic generic stuff. Specific tasks will exist in the child classes. 
    Upon initialization the host, user, password and database will be provided."""

    def __init__(self, host: str, user: str, password: str, database: str = None) -> None:
        self.__host = host
        self.__user = user
        self.__password = password
        self.database=database
        try:
            self.__conn = mc.connect(host=self.__host, user=self.__user, password=self.__password, database = self.database)
            self.__cursor =self.__conn.cursor()
        except mc.Error as e:
            print(f"Buddy, I just tested the connection and something is very wrong. Most likely the credentials. Here's what's wrong:\n{e}")
            exit()

    # I need this because child classes can't access private attributes and I am not going to rewrite this pile of shit
    def getConn(self):
        return self.__conn
    

    def getCursor(self):
        return self.__cursor


    def setDatabase(self, database: str) -> None:
        """This just sets the database variable to something else. It doesn't create a database. To do that, use createDatabase method. That creates a database AND sets the database variable to the newly created database"""
        self.database = database
        #this needs to be reasigned just in case it was "None" before
        self.__conn = mc.connect(host=self.__host, user=self.__user, password=self.__password, database = self.database)
        self.__cursor =self.__conn.cursor()


    def createDatabase(self, database: str, overwrite: bool = True) -> None:
        """Creates a database from scratch. It has two variables: a string for the name of the database and a bool to decide weather or not to delete if the database exists. By default this is set to true. Meaning by default it will drop the database and create it again."""
        if overwrite:
            self.__cursor.execute(f"DROP SCHEMA IF EXISTS `{database}`")
            self.__cursor.execute(f"CREATE SCHEMA `{database}`")
        else:
            self.__cursor.execute(f"CREATE SCHEMA IF NOT EXISTS `{database}`")
        self.__conn.commit()
        self.database = database
        #this needs to be reasigned just in case it was "None" before
        self.__conn = mc.connect(host=self.__host, user=self.__user, password=self.__password, database = self.database)
        self.__cursor =self.__conn.cursor()


    def deleteDatabase(self) -> None:
        """This will just delete the entire database, no questions asked."""
        self.__cursor.execute(f"DROP SCHEMA `{self.database}`")
        self.__conn.commit()
        self.database = None
        self.__conn = mc.connect(host=self.__host, user=self.__user, password=self.__password)
        self.__cursor =self.__conn.cursor()


    def createTable(self, data: dict, overwrite: bool = True) -> None:
        """Expects a dictionary with the structure {name: name of the table, columns:{column name: column setting}}. The ID and the primary key is set automatically It also has a optional boolean parameter to overwrite or not if the table already exists. The default is set to True."""
        
        tableData = "`id` INT UNSIGNED NOT NULL AUTO_INCREMENT, "
        for k, v in data["columns"].items():
            tableData += f"`{k}` {v} NULL, "
        tableData += "PRIMARY KEY (`id`), UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE"

        if overwrite:
            self.__cursor.execute(f"DROP TABLE IF EXISTS `{data["name"]}`;")
            self.__cursor.execute(f" CREATE TABLE `{data["name"]}` ({tableData});")
        else:
            self.__cursor.execute(f"CREATE TABLE IF NOT EXISTS `{data["name"]}` ({tableData});")
        self.__conn.commit()


    def deleteTable(self, table: str) -> None:
        """This will delete the tale from the database. All of it. Requires only the table name."""
        self.__cursor.execute(f"DROP TABLE `{table}`")
        self.__conn.commit()


    def wipeTable(self, table: str) -> None:
        self.__cursor.execute(f"TRUNCATE `{table}`")
        self.__conn.commit()


    def addEntry(self, table: str, data: dict) -> None:
        dictItems = data.items()
        columns = ""
        values = ""
        for i in dictItems:
            columns += f"`{dictItems[0]}`, "
            values += f"'{dictItems[1]}', "
        self.__cursor.execute(f"INSERT INTO `{table}` ({columns[:-1]}) VALUES ({values[:-1]}); ")
        self.__conn.commit()


    def removeEntry(self, table, id: int) -> None:
        self.__cursor.execute(f"DELETE FROM {table} WHERE (`Id` = {id})")
        self.__conn.commit()


    def editEntry(self, id: int, table: str, data: dict) -> None:
        dictItems = data.items()
        query = ""
        for i in dictItems:
            query += f"`{dictItems[0]}` = '{dictItems[1]}', "
        # TODO: Warning, this is not ok. This is wrong. Check the MYSQL command. it hs to be set `something` = "something"!!
        self.__cursor.execute(f"UPDATE `{table}` SET {query[:-1]} WHERE (`Id` = '{id}')")
        self.__conn.commit()
    
