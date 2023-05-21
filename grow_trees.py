from sql_engine import SQLEngine
from plant import Plant
import time
import os

def grow_trees():
    conn = SQLEngine(host=os.environ["MYSQL_HOST"], user=os.environ["MYSQL_USER"], passwd=os.environ["MYSQL_PASSWORD"], db="DLPlant")

    user_list = conn.get_grow_list()
    print(f"Num of users to grow: {len(user_list)}")
    for user in user_list:
        user_details = conn.get_user(guild_id=user[0], member_id=user[1])
        plant = Plant(plant_type="random_basic_plant", random=True, random_choices=2, new_start=user_details[1])
        plant.grow(1)
    
        conn.update_user(guild_id=user[0], member_id=user[1], iter=user_details[0] + 1 ,curr_string=plant.l_system.current)
    
    print("Done growing trees.")

if __name__ == "__main__":
    
    SLEEP_TIME = 60 # 1 minute
    while True:
        start_time = time.time()
        grow_trees()
        end_time = time.time()
        if (SLEEP_TIME - (end_time - start_time) < 0):
            continue
        time.sleep(SLEEP_TIME - (end_time - start_time))