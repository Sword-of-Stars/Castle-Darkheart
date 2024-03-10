from PIL import Image, ImageDraw, ImageChops

def create_radial_gradient(size, center, color, transparency):
    # Create a new RGBA image
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Calculate the distance from each pixel to the center
    for x in range(size[0]):
        for y in range(size[1]):
            distance = ((x - center[0])**2 + (y - center[1])**2)**0.5

            # Calculate the alpha (transparency) value based on the distance
            alpha = int(255 * (1 - distance / (size[0] / 2)))

            # Set the pixel color with transparency
            pixel_color = color + (alpha,)
            draw.point((x, y), fill=pixel_color)

    return image

# Set the parameters
image_size = (50, 50)
gradient_center = [x//2 for x in image_size]
gradient_color = (255, 255, 255)  # white color
gradient_transparency = 0.5  # Set transparency between 0 (fully transparent) and 1 (fully opaque)

# Create the radial gradient image
gradient_image = create_radial_gradient(image_size, gradient_center, gradient_color, gradient_transparency)

# Save or display the image
gradient_image.save("data/radial_gradient.png")
