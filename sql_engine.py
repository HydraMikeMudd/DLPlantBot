import MySQLdb



class SQLEngine:
    def __init__(self, host: str, user: str, passwd: str, db: str):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db)
        self.cursor = self.conn.cursor()

    def exec_sql(self, sql: str, params: tuple = None):
        try:
            self.cursor.execute(sql, params)
        except Exception as e:
            print(e)
            raise e

        self.commit()
    
    def close(self):
        if self.conn:
            self.conn.close()

    def commit(self):
        if self.conn:
            self.conn.commit()

    def rollback(self):
        if self.conn:
            self.conn.rollback()

    def __del__(self):
        self.close()

    def __enter__(self):
        if self.cursor == None:
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.close()

    def check_for_user(self, guild_id: int, member_id: int):
        
        sql = "SELECT guild_id, member_id FROM users WHERE guild_id = %s AND member_id = %s"

        self.exec_sql(sql, (guild_id, member_id))

        result = self.cursor.fetchone()
        if result:
            return True

        return False
    
    def create_new_user(self, guild_id: int, member_id: int, iter: int, curr_string: str):

        sql = "INSERT INTO users (guild_id, member_id, iteration, curr_sentence, grow) VALUES (%s, %s, %s, %s, 0)"

        self.exec_sql(sql, (guild_id, member_id, iter, curr_string))
        return self.check_for_user(guild_id, member_id)
    
    def get_user(self, guild_id: int, member_id: int):
        sql = "SELECT iteration, curr_sentence, grow FROM users WHERE guild_id = %s AND member_id = %s"

        self.exec_sql(sql, (guild_id, member_id))

        result = self.cursor.fetchone()
        return result
    
    def get_user_grow(self, guild_id: int, member_id: int):
        sql = "SELECT grow FROM users WHERE guild_id = %s AND member_id = %s"

        self.exec_sql(sql, (guild_id, member_id))

        result = self.cursor.fetchone()
        return result
    
    def update_user(self, guild_id: int, member_id: int, iter: int, curr_string: str):
        sql = "UPDATE users SET iteration = %s, curr_sentence = %s, grow = 0 WHERE guild_id = %s AND member_id = %s"

        self.exec_sql(sql, (iter, curr_string, guild_id, member_id))

    def set_user_grow(self, guild_id: int, member_id: int, grow: int):
        sql = "UPDATE users SET grow = 1 WHERE guild_id = %s AND member_id = %s"

        self.exec_sql(sql, (grow, guild_id, member_id))