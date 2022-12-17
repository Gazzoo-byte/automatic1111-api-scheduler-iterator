import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
imgnum = 0

url = "http://127.0.0.1:7860"
sched_index = ["Euler a","Euler","LMS","Heun","DPM2","DPM2 a","DPM++ 2S a","DPM++ 2M","DPM++ SDE","DPM fast","DPM adaptive", "LMS Karras","DPM2 Karras","DPM2 a Karras","DPM++ 2S a Karras","DPM++ 2M Karras","DPM++ SDE Karras","DDIM","PLMS"]

def iter_scheds(a):
    payload = {
        "prompt": "a dog",
        "negative_prompt": "",
        "steps": 40,
        "width": 512,
        "height": 512,
        "seed": 1,
        "sampler_name": a,
    }
    print(a+" starting")

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
        
    r = response.json()

    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        image.save(f"output{a}.png", pnginfo=pnginfo)
    print(a+" done")


for x in sched_index:
    iter_scheds(x)
