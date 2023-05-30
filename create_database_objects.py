import MySQLdb
import os
import dotenv

dotenv.load_dotenv()

conn = MySQLdb.connect(host=os.environ["MYSQL_HOST"], user=os.environ["MYSQL_USER"], passwd=os.environ["MYSQL_PASSWORD"])
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS DLPlant;")

conn.commit()

cursor.execute("USE DLPlant;")

cursor.execute("""DROP TABLE IF EXISTS users;""")

cursor.execute("""CREATE TABLE users (
  guild_id bigint NOT NULL,
  member_id bigint NOT NULL,
  iteration int,
  curr_sentence mediumtext,
  grow tinyint(1),
  img_path varchar(255),
  CONSTRAINT PK_Users PRIMARY KEY (guild_id,member_id)
);""")


conn.commit()
conn.close()