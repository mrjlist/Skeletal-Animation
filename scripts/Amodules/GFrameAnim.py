import base64



def GenerateFrameAnimation(InFF, OuFF):

    
    encoded_string = base64.b64encode(open(InFF, "rb").read()).decode("utf-8")

    

def createQ(encoded_img, width, height):

    quest = {
        "width": width,
        "height": height,
        "save_images": False,
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
