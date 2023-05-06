import base64
import os, shutil
from PIL import Image
import requests
url = "http://127.0.0.1:7860"



def GenerateFrameAnimation(InFF, OuFF):

    imgDirList = [f"{InFF}\{img}" for img in os.listdir(InFF)]

    for imgN in range(len(imgDirList)):

        encoded_string = base64.b64encode(open(imgDirList[imgN], "rb").read()).decode("utf-8")

        img = Image.open(imgDirList[imgN])
        width, height = img.size

        requests.post(url=f'{url}/sdapi/v1/txt2img', json=createQ(encoded_string, width, height))

        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(base_dir, '..', '..', '..', 'outputs', 'txt2img-images', 'detected_maps', 'openpose_hand')
        files = os.listdir(img_dir)

        suffix = '.png'
        old_path = f"{img_dir}\{files[len(files)-1]}"
        new_pathName = f"{OuFF}\{str(imgN) + suffix}"

        shutil.move(old_path, new_pathName)

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

# GenerateFrameAnimation(r'C:\Users\andre\Desktop\IMG_4958', r"C:\Users\andre\Desktop\render")