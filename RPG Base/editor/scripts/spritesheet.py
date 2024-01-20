from PIL import Image

# This takes large images from the ms paint files and clips out important sections

COLORKEY = (0,0,0)
SECTION_START = (0,255,0, 255)
SECTION_END = (255, 0, 0, 255)

#SECTION_START = (0,255,0)
#SECTION_END = (255, 0, 0)

start = []
end = []
sections = []

def get_section(spritesheet):
    width, height = spritesheet.size
    for x in range(width):
        for y in range(height):
            c = spritesheet.getpixel((x, y))
            if c == SECTION_START:
                start.append([x,y])
            elif c == SECTION_END:
                end.append([x,y])

    #print(f"Number of images: {len(start)}")

    final_images = []
    for i in range(len(start)):
        img = spritesheet.crop([start[i][0]+1, start[i][1]+1, end[i][0], end[i][1]])
        #img.save(f"tileset/test_{i}.png")
        final_images.append(img)

    return final_images

def stitch_images(images, name="test", folder="tileset"):
    # Open all the images and get their dimensions
    widths, heights = zip(*(i.size for i in images))

    # Determine the total size of the final image
    total_width = sum(widths)
    max_height = max(heights)

    # Create a new image with the calculated dimensions
    new_image = Image.new('RGB', (total_width, max_height))

    # Paste the images into the new image
    x_offset = 0
    for i, img in enumerate(images):
        new_image.paste(img, (x_offset, 0))
        x_offset += img.size[0]

    # Save the final image as a PNG file
    new_image.save(f'{folder}/{name}.png')

if __name__=="__main__":
    with Image.open("blue_decor.png") as img:
        stitch_images(get_section(img), name="cave_decors", folder="data/images/decor")