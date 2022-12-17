import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin

url = "http://127.0.0.1:7860" #Where the API lives
sched_index = ["Euler a","Euler","LMS","Heun","DPM2","DPM2 a","DPM++ 2S a","DPM++ 2M","DPM++ SDE","DPM fast","DPM adaptive", "LMS Karras","DPM2 Karras","DPM2 a Karras","DPM++ 2S a Karras","DPM++ 2M Karras","DPM++ SDE Karras","DDIM","PLMS"]

def iter_scheds():
    payload = {
        "prompt": "a dog", #Your prompt, optional
        "negative_prompt": "", #Your negative prompt, optional
        "steps": 10, #Number of steps to do
        "width": 256, #Width, must be a multiple of 2
        "height": 256, #Height, must be a multiple of 2
        "seed": 1, #RNG seed, can be set to -1 for random but not recommended
        "sampler_name": x, #Gets the scheduler from the index
    }
    print(x+" starting") #Logs job start
    
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload) #Send above payload to API start
        
    r = response.json() #End
    
    try:
        for i in r['images']: #Download image start
            image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

            png_payload = {
                "image": "data:image/png;base64," + i
            }
            response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("parameters", response2.json().get("info"))
            image.save(f"output{x}.png", pnginfo=pnginfo)
        print(x+" done") #end
    except KeyError: #Scheduler error handling
        print(f"Something went wrong with {x}, is it unavailable or misspelt? Scheduler names are case sensitve")  
    except: #Everything else error handling
        print(f"Something I've not seen before went wrong with {x}")


modelpayload = {
    "sd_model_checkpoint": "Anything-V3.0-pruned.ckpt [2700c435]", #Set the model here
}
try:
    print(f"setting model to {modelpayload}")
    response = requests.post(url=f'{url}/sdapi/v1/options', json=modelpayload) #Set the model in the API start
    r = response.json() #end
except:
    print("Something went wrong while setting the model, reverting to default")

for x in sched_index:
    try:
        iter_scheds() #Iterate through the scheduler index
    except KeyboardInterrupt: #Catch Ctrl-c to quit early
        print("Keyboard interrupt received, exiting...")
        exit()
    except: #Something went wrong before talking to the API
        print("Something went catastrophically wrong")
