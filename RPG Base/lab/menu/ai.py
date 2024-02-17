import torch
from diffusers import StableDiffusionXLImg2ImgPipeline
from diffusers.utils import load_image

pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-refiner-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
)
pipe = pipe.to("cuda")

init_image = load_image("lab/menu/menu_screen.png").convert("RGB")
prompt = "an evil gothic castle"
image = pipe(prompt, image=init_image).images
print(image)
image[0].show()