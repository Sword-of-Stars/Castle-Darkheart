from PIL import Image

def find_all_colors(image):
    """Finds all unique colors in an image and returns them as a set."""
    colors = set()
    pixels = image.getdata()
    for pixel in pixels:
        colors.add(pixel)
    return colors

def swap_pixel_color(image, original_color, new_color):
    """Swaps all pixels of a specified color to a new color in an image."""
    pixels = image.load()
    width, height = image.size
    for x in range(width):
        for y in range(height):
            if pixels[x, y][:3] == original_color:
                pixels[x, y] = new_color

def main():
    image = Image.open("Level Editor/data/tileset_03.png")

    print(find_all_colors(image))

    # 2. Allow user to swap colors
    #while True:
        #original_color = tuple(map(int, input("Enter the color to swap (R, G, B): ").split(",")))
        #new_color = tuple(map(int, input("Enter the new color (R, G, B): ").split(",")))
    for orig, new in swap:
        swap_pixel_color(image, orig, new)

        #image.show()

    image.save("hello.png")

# (65,50,69)

swap = [[(92,92,92),(100,79,112)], [(54,54,54),(65,50,79)], [(89,81,80),(106,74,112)], [(89,80,81),(106,74,112)],[(79,79,79),(84,62,94)],[(60,53,60),(66,41,77)],[(83,9,89),(66,41,77)],
 [(117,117,117),(114,97,130)], [(112,101,102),(114,97,130)], [(127,127,127),(102,81,120)],[(156,156,156),(114,97,130)]]

if __name__ == "__main__":
    main()
