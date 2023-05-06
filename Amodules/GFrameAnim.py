import base64
import os
from PIL import Image
import requests
url = "http://127.0.0.1:7860"



def GenerateFrameAnimation(InFF, OuFF):
    print(InFF)
    print("-----------------------------------------------------------------------------------------------------")
    encoded_string = base64.b64encode(open(InFF, "rb").read()).decode("utf-8")

    img = Image.open(InFF)

    width, height = img.size

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=createQ(encoded_string, width, height))
    r = response.json()

def createQ(encoded_img, width, height):

    quest = {
        "width": width,
        "height": height,
        "save_images": False,
        "steps": 0,
        "alwayson_scripts": {
            "controlnet": {
                "args": [
                    {
                        "input_image": "data:image/png;base64," + f"{encoded_img}",
                        "module": "openpose_hand",
                        "model": 'control_v11p_sd15_openpose [cab727d4]',
                        "weight": 1,
                        "processor_res": 1024,
                        "guidance_start": 0,
                        "guidance_end": 1
                    }
                ]
            }
        }
    }

    return quest
