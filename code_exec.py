import json
import random

collections = []
env = ""
data = {}

def set_collection(value):
    global collections
    collections = value

def set_env(value):
    global env
    env = value

def load_data():
    for collection in collections:
        with open(f"tau_bench/envs/{env}/data/{collection}.json", "r") as f:
            data[collection] = json.load(f)

def get_data():
    return data

def get_random(collection):
    element_id = random.choice(list(data[collection].keys()))
    return (element_id, data[collection][element_id])

def get_random_user():
    user = get_random("users")
    print("User ID:")
    print(user[0])
    print("User data:")
    print(json.dumps(user[1], indent=2))
