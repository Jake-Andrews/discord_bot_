from queue import Empty
import sqlite3
import discord

class DatabaseHelper():
    def __init__(self):
        self.dbCon = sqlite3.connect('database/userstorage.db')
        self.dbCursor = self.dbCon.cursor()

    def query_deleted_messages(self, guild_id, user_id):
        sql = f"SELECT msg FROM (_{guild_id}) WHERE user_id = {user_id} AND deleted_or_not = {1}"

        try:
            self.dbCursor.execute(sql)
            result = self.dbCursor.fetchall()
        except sqlite3.DatabaseError as e:
            print(f"Error: {e.args[0]}")          
        
        if not result:
            return f"nodeletedmessages"

        else: return result

    def update_deleted_message(self, message):
        sql = "UPDATE _"
        sql += str(message.guild.id)
        sql += """ SET deleted_or_not = ? WHERE message_id = ?"""
        values = (1, str(message.id))
        print(f"message_id: {message.id}")

        try:
            self.dbCursor.execute(sql, values)
            self.dbCon.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error: {e.args[0]}")
        

    def query_edited_messages(self, guild_id, msg_id):
        sql = f"SELECT msg FROM (_{guild_id}) WHERE message_id = {msg_id}"

        try:
            self.dbCursor.execute(sql)
            result = self.dbCursor.fetchall()

        except sqlite3.DatabaseError as e:
            print(f"Error: {e.args[0]}")
            return "Database error"
        print(f"Result:  {result}")

        print(f"result: {result[0]}")
        print(f"result[0][0]: {result[0][0]}")
        if result is None:
            return "noedit"

        elif result[0][0] == "":
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
     
    def insert_message_edit(self, before_message, after_message):
        #string is the id of our bot
        print(f"before: {after_message.content}")
        if after_message.author.id == "922987264261390376":
            return	
        
        #print(f"after_content: {after_content}, guild_id: {guild_id}, edited_at_time: {edited_at_time}")
        guild_id = str(after_message.guild.id)
        sql = "INSERT INTO _"
        sql += guild_id
        sql += "(msg, message_id, channel_id, edited_or_not, user_id, edited_time, published_time, deleted_or_not) VALUES(?,?,?,?,?,?,?,?)"
        val = (after_message.content, str(after_message.id), str(after_message.channel), 1, str(after_message.author.id), after_message.edited_at, before_message.created_at, 0)
        
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
        sql += """ (msg, message_id, channel_id, edited_or_not, user_id, edited_time, published_time, deleted_or_not) VALUES(?,?,?,?,?,?,?,?)"""
        val = (message_content, message_id, channel_id, 0, user_id, "", edited_time, 0)
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
        user_id TEXT, 
        edited_time TEXT, 
        published_time TEXT, 
        deleted_or_not INTEGER     
        )
        """ 

        self.dbCursor.execute(sql)
        self.dbCon.commit()