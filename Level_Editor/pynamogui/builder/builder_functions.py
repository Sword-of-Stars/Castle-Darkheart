import os
import json

def load_json(path):
    with open(path, "r") as load_file:
        file = json.load(load_file)
    return file

def get_config(folder_path):
    file_path = os.path.join(folder_path, 'config.json')  # Construct the file path

    if not os.path.exists(file_path):
        json_data = json.dumps({})
        with open(file_path, 'w') as json_file:
            json_file.write(json_data)

    return load_json(file_path)

def get_path_id(config_path, path):
    json_data = load_json(config_path)

    key = next((k for k, v in json_data.items() if v == path), None)

    if key is None:
        largest_key = int(max(json_data.keys()) if json_data.keys() else 0)

    # Create a new key-value pair
        new_key = largest_key+1 if largest_key != 0 else 0
        json_data[new_key] = path
        #print(f"Created new key '{new_key}' with value '{path}'")
        key = new_key
    #else:
        #print(f"Key '{key}' exists with value '{path}'")

    json_string = json.dumps(json_data)
    with open(config_path, "w") as json_file:
        json_file.write(json_string)

    return key

def get_images_from_db(db, path_id):
    images = []
    for key, item in db.items():
        if path_id == key.split(";")[1]:
            images.append(item)
    return images
      
def generate_id(type, path, index, config_path):
    if type == 'spritesheet':
        method = 'ss'
    else:
        method = 'xx'
    
    return f"{method};{get_path_id(config_path, path)};{index}"

def read_id(ID, config_path):
    method, path, index = ID.split(".") # ex. ss.000.002

def save_json(data, path):
    json_string = json.dumps(data)
    with open(f"{path}.json", "w") as json_file:
        json_file.write(json_string)

#-- Non-universalized World Transforms --#
CHUNK_DIVISOR = 4
SIZE = 64

def screen_to_world(screen_coords, offset, SIZE=SIZE, scale=1):
    screen_x, screen_y = screen_coords
    offset_x, offset_y = offset
    world_x = (screen_x/scale) + offset_x
    world_y = (screen_y/scale) + offset_y
    return [int(world_x//SIZE), int(world_y//SIZE)]

def get_chunk_id2(pos):
    x, y = pos
    #divisor = CHUNK_SIZE/SIZE
    divisor = CHUNK_DIVISOR
    return (x//divisor, y//divisor)

def screen_to_chunk2(pos, offset, scale=1):
    return get_chunk_id2(screen_to_world(pos, offset, scale=scale))

