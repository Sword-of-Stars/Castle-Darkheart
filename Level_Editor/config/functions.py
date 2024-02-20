import os
import json

def change_page(gui, page):
    gui.current_page = page
    
def change_visible_regions(gui, off, on):
    current_page = gui.pages[gui.current_page]
    for region in off: 
        current_page.regions[region].visible = False
    for region in on: 
        current_page.regions[region].visible = True

def change_palette(gui, config):
    gui.builder.palette.get_images(config)

def save_file(map_data, path):
    name = input("Name your file: ") # Make a UI feature later
    json_string = json.dumps(map_data)
    with open(f"{path}/{name}.json", "w") as json_file:
        json_file.write(json_string)
    
def load_file(builder, path="maps"):

    try:
        name = input("Name the file you'd like to load: ") # Make a UI feature later
        with open(f"{path}/{name}.json", "r") as load_file:
            file = json.load(load_file)
            
    except:
        print(f"Sorry, {name} is not a valid file name.")

    try:
        builder.current_map = file
    except:
        print("Uh, boss? Something went wrong ...")



def new_map(size):
    # In the future, perhaps include additional data, such as the map name, 
    # or other important ID info
    map_data = {"SIZE":size, "map_data":{}}
    print(size)
    return map_data

def go_to_settings():
    print("Moving, sarge!")

