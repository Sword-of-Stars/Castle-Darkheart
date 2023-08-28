import json

my_dict = {"speed":6,"damage":7}

name = 'player_config'
with open(f"scripts/{name}.json", "w") as save_file:
    json.dump(my_dict, save_file)