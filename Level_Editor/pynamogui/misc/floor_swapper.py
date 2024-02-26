import json
import random

def load_file(name, path="../RPG_Base/maps"):

    try:
        with open(f"../RPG_Base/maps/{name}.json", "r") as load_file:
            file = json.load(load_file)
            return file

            
    except:
        print(f"Sorry, {name} is not a valid file name.")
        return 
    
def new_tile(n, pos):
    return {'tile_ID': f'ss;1;{n}', 'group': 'tile', 'z-order': 0, 'pos': pos, 'offset': [0, 0], 'sum': 0, 'auto?': 0}

def save_file(map_data, path="../RPG_Base/maps"):
    json_string = json.dumps(map_data)
    with open(f"../RPG_Base/maps/floor_swap.json", "w") as json_file:
        json_file.write(json_string)


map_file = load_file("iter5")

choices = [x for x in range(1,10)]
blank_chance = 1

for key, item in map_file["chunks"].items():
    for tile in item:
        if tile["tile_ID"] == "ss;1;0":
            for overhang in item:
                if "ss;0" in overhang["tile_ID"] and overhang["z-order"] == 1 and overhang["pos"] == tile["pos"]:
                    break
            else:
                # place a floor tile
                if random.randint(0,20) > blank_chance:
                    choice = random.choices(choices, weights=[1,.1,.3,.1,.1,.1,.1,.1,.1])
                    item.append(new_tile(choice[0], tile["pos"]))


save_file(map_file)
