import sqlite3
import database

class DatabaseHelper():
    def __init__(self):
        self.dbCon = sqlite3.connect('database/userstorage.db')
        self.dbCursor = self.dbCon.cursor()

    def query_edited_messages(self, guild_id, msg_id):
        sql = f"SELECT msg,edited_contents FROM (_{guild_id}) WHERE message_id = {msg_id}"

        try:
            self.dbCursor.execute(sql)
            result = self.dbCursor.fetchall()

        except sqlite3.DatabaseError as e:
            print(f"Error: {e.args[0]}")
            return "Database error"
        print(f"result: {result[0]}")
        print(f"result[0][0]: {result[0][0]}")
        if result[0][1] == "":
            return "noedit"

        else: return result

    def query_users_history(self, guild_id, users_id):
        sql = f"SELECT msg FROM (_{guild_id}) WHERE user_id = {users_id}"

        try: 
            self.dbCursor.execute(sql)
            result = self.dbCursor.fetchall()
        
        except sqlite3.DatabaseError as e:
            print(f"Error: {e.args[0]}")
        
        return result
     
    def insert_message_edit(self, author_id, message_id, guild_id, edited_at_time, after_content):
        #string is the id of our bot
        if author_id == "922987264261390376":
            return	
        
        print(f"after_content: {after_content}, guild_id: {guild_id}, edited_at_time: {edited_at_time}")

        sql = f"UPDATE _{guild_id} SET edited_or_not = ?, edited_contents = ?, edited_time = ? WHERE message_id = {message_id}"
        val = (1, after_content, edited_at_time)
        print(f"After: {after_content}")
        try:
            self.dbCursor.execute(sql, val)
            self.dbCon.commit()

        except sqlite3.DatabaseError as e:
            print(f"Error: {e.args[0]}")
    
    def insert_message(self, message_content, message_id, channel_id, user_id, edited_time, guild_id):
        if user_id == "922987264261390376":
                return 

        sql = "INSERT INTO _"
        sql += guild_id
        sql += """ (msg, message_id, channel_id, edited_or_not, edited_contents, user_id, edited_time, published_time) VALUES(?,?,?,?,?,?,?,?)"""
        val = (message_content, message_id, channel_id, 0, "", user_id, "", edited_time)
        try:
            self.dbCursor.execute(sql, val)
            self.dbCon.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error: {e.args[0]}")
    
    def insert_guild(self, guild_id):
        #When the bot joins a guild, create a new table with the guilds id

        sql = "CREATE TABLE IF NOT EXISTS _"
        sql+= guild_id
        sql+=""" (
        msg TEXT,
        message_id TEXT,
        channel_id TEXT, 
        edited_or_not INTEGER, 
        edited_contents TEXT, 
        user_id TEXT, 
        edited_time TEXT, 
        published_time TEXT     
        )
        """ 
        val = (guild_id,)

        self.dbCursor.execute(sql, val)
        self.dbCon.commit()