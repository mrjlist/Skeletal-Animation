from PIL import Image, PngImagePlugin
import requests
import io
import base64

url = "http://127.0.0.1:7860"

def gt():
    from PIL import Image, PngImagePlugin
    import requests
    import io
    import base64

    encoded_string = base64.b64encode(open("C:\\Users\\andre\\Desktop\\IMG_4958\\00062.png", "rb").read()).decode("utf-8")

    # decoded_image = Image.open(io.BytesIO(base64.b64decode(encoded_string)))

    # # Показать openpose_hand

    # decoded_image.show()

    quest = {
        "denoising_strength": 1,
        "prompt": "<lora:blindbox_v1_mix:1.4>, the girl amigurumi is cute against the background of the city in the style of cyberpunk",
        "styles": [],
        "seed": -1,
        "subseed": -1,
        "subseed_strength": 0,
        "seed_resize_from_h": -1,
        "seed_resize_from_w": -1,
        "sampler_name": "Euler a",
        "steps": 0,
        "cfg_scale": 7,
        "width": 512,
        "height": 1024,
        "negative_prompt": "(deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4), disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation",
        "sampler_index": "Euler a",
        "save_images": False,
        "alwayson_scripts": {
        "controlnet": {
        "args": [
            {
                "input_image": "data:image/png;base64," + f"{encoded_string}",
                "module": "openpose_hand",
                "model": 'control_v11p_sd15_openpose [cab727d4]',
                "weight": 1,
                "processor_res": 512,
                "guidance_start": 0.2,
                "guidance_end": 1
            }
        ]
        }
    }
    }
    import json

    # Открываем файл JSON для записи
    # with open('output.json', 'w') as f:
        # Записываем словарь в файл в формате JSON
        # json.dump(quest, f)
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=quest)
    # response = requests.get(url=f'{url}/controlnet/model_list')
    print(response.json())

    # for i in r['images']:
    #     image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
    
def filet():
    import os
    from PIL import Image

    startFileGMask = ""

    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(base_dir, '..', '..', '..', 'outputs', 'txt2img-images', 'detected_maps', 'openpose_hand')
        files = os.listdir(img_dir)

        startFileGMask = int(files[len(files)-1][14:-4])
    except:
        startFileGMask = None
    
    print(startFileGMask)


    path = r'C:\Users\andre\Desktop\IMG_4958'

    for img in [f"{path}\{img}" for img in os.listdir(path)]:

        # Открываем изображение
        img = Image.open(img)

        width, height = img.size

        # print(f'Размер изображения: {width} x {height}')

        import os
        import shutil

        source_dir = 'source'  # путь к исходной папке
        dest_dir = 'destination'  # путь к папке, куда нужно переместить изображения
        suffix = '.png'  # расширение для новых имен файлов

        # Создаем папку назначения, если она не существует
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # Получаем список файлов в исходной папке
        files = os.listdir(source_dir)

        # Счетчик для новых имен файлов
        count = 1

        # Проходимся по списку файлов
        for file in files:
            # Проверяем, что файл - изображение
            if file.endswith('.jpg'):
                # Формируем новое имя файла
                new_name = str(count) + suffix
                
                # Полный путь к исходному файлу
                old_path = os.path.join(source_dir, file)
                
                # Полный путь к файлу назначения
                new_path = os.path.join(dest_dir, new_name)
                
                # Копируем файл в папку назначения и переименовываем его
                shutil.copy(old_path, new_path)
                
                # Увеличиваем счетчик для новых имен файлов
                count += 1



# filet()