from core.sql_engine import SQLEngine
from core.sql_engine import UserDetails
from core.plant import Plant
from core.image_loader import write_image_path
import time
import os
import dotenv

dotenv.load_dotenv()

def grow_trees():
    conn = SQLEngine(host=os.environ["MYSQL_HOST"], user=os.environ["MYSQL_USER"], passwd=os.environ["MYSQL_PASSWORD"], db="DLPlant")

    create_trees_list = conn.get_empty_path_list()
    print(f"Num of missing images to create: {len(create_trees_list)}")
    for user in create_trees_list:
        user_details = conn.get_user(guild_id=user[0], member_id=user[1])
        plant = Plant(plant_type="random_basic_plant", random=True, random_choices=5, new_start=user_details[1])
        data_stream = plant.plot_plant()
        filepath = write_image_path(filepath=user_details[UserDetails.IMG_PATH], data=data_stream)
        conn.update_user(guild_id=user[0], member_id=user[1], iter=user_details[UserDetails.ITERATION] ,curr_string=plant.l_system.current, filepath=filepath)

    user_list = conn.get_grow_list()
    print(f"Num of users to grow: {len(user_list)}")
    for user in user_list:
        user_details = conn.get_user(guild_id=user[0], member_id=user[1])
        plant = Plant(plant_type="random_basic_plant", random=True, random_choices=5, new_start=user_details[1])
        plant.grow(1)
        data_stream = plant.plot_plant()
        filepath = write_image_path(filepath=user_details[UserDetails.IMG_PATH], data=data_stream)
        conn.update_user(guild_id=user[0], member_id=user[1], iter=user_details[UserDetails.ITERATION] + 1 ,curr_string=plant.l_system.current, filepath=filepath)
    
    print("Done growing trees.")

if __name__ == "__main__":
    
    SLEEP_TIME = 60 # 1 minute
    while True:
        start_time = time.time()
        try:
            grow_trees()
        except Exception as e:
            with open("error_log.txt", "a") as f:
                f.write(f"{time.ctime()}: {e}\n")
        end_time = time.time()
        if (SLEEP_TIME - (end_time - start_time) < 0):
            continue
        time.sleep(SLEEP_TIME - (end_time - start_time))