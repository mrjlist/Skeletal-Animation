from PIL import Image, PngImagePlugin
from gradio.outputs import Image
import requests
import json
import io
import base64
from modules.sd_samplers import samplers

url = "http://127.0.0.1:7860"
def GenerateStartFrames(prompt, n_prompt, sampler_index, steps, seed_resize_from_w, seed_resize_from_h, cfg_scale, seed, prompt_styles):
    quest = {
        # "denoising_strength": 0,
        "prompt": prompt,
        "styles": prompt_styles,
        "seed": -1,
        "subseed": -1,
        "subseed_strength": 0,
        "seed_resize_from_h": -1,
        "seed_resize_from_w": -1,
        "sampler_name": samplers[sampler_index].name,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "width": seed_resize_from_w,
        "height": seed_resize_from_h,
        "negative_prompt": n_prompt,
        "sampler_index": samplers[sampler_index].name,
        "save_images": True,
        }
    print(quest)
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=quest)
    r = response.json()
    
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
    Image(image)
    # return image