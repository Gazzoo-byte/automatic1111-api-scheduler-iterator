import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin

url = "http://127.0.0.1:7860" #the url where the api lives

#List of all provided schedulers
sched_index = ["Euler a","Euler","LMS","Heun","DPM2","DPM2 a","DPM++ 2S a","DPM++ 2M","DPM++ SDE","DPM fast","DPM adaptive", "LMS Karras","DPM2 Karras","DPM2 a Karras","DPM++ 2S a Karras","DPM++ 2M Karras","DPM++ SDE Karras","DDIM","PLMS"]

#Function to contain generation and retrieval of images from stable diffusion
def iter_scheds(a):
    payload = {
        "prompt": "a dog", #prompt goes here
        "negative_prompt": "", #negative prompt if you use one
        "steps": 40, 
        "width": 512,
        "height": 512,
        "seed": 1, #recommend using a fixed seed here for better comparison of each scheduler
        "sampler_name": a, #gets the scheduler name from the variable
    }
    print(a+" starting") #prints to the cli which scheduler is starting

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload) #passes above payload to the api
        
    r = response.json() 

    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        image.save(f"output{a}.png", pnginfo=pnginfo) #saves the output with the scheduler in the filename
    print(a+" done") #prints to the cli that the scheduler has finished


for x in sched_index: #loop through each scheduler in the collction
    iter_scheds(x) #passes the scheduler to the function
