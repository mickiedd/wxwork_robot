from os import listdir
from os.path import isfile, join
import urllib.request
import json 
import random
import base64
import hashlib
import sched, time

rootimagepath = 'drinkwaterimages'
url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a46aa2fe-df89-456e-92d4-3061fb82b042"
freq = 15 # 秒
def md5f(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
def drinkWater():
    images_url = [f for f in listdir(rootimagepath) if isfile(join(rootimagepath, f))]
    image_url = rootimagepath + "/" + images_url[random.randint(0,len(images_url) - 1)]
    with open(image_url, "rb") as image_file:
        image_content = image_file.read()
        encoded_string = base64.b64encode(image_content)
    md5 = md5f(image_url)
    encoded_string = encoded_string.decode('UTF-8')
    data = {'msgtype': 'image', 
            "image": {
                "base64": encoded_string,
                "md5": md5
            }
           }     
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(data)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(req, jsondataasbytes)
    print(response.read())

s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 
    print("Start Drink Water...")
    drinkWater()
    # do your stuff
    s.enter(freq, 1, do_something, (sc,))
drinkWater()
s.enter(freq, 1, do_something, (s,))
s.run()