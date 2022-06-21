"Take picture with wand"
from pathlib import Path
import requests


WAND="10.11.131.232"
URL="http://"+WAND+":8080/pic/still?flash=1"

def take_picture(url, filepath, zoom=None):
    "take a picture from wand"
    local_filename = filepath
    #print(url)
    if zoom:
        url = url + "&zoom=" + str(zoom)
    resp = requests.get(url)
    if resp:
        #print(resp.request.headers)
        #print(resp.content)
        with open(local_filename, 'wb') as fd:
            fd.write(resp.content)
        return True
    else:
        print("Error", resp)

def take_serie(path, number=10, zoom=None):
    "take a serie of pictures to folder"
    for i in range(number):
        filename = Path(path) / f'pic_{i:02}.jpg'
        print(filename)
        input("Press Enter to take picture")
        take_picture(URL, filename, zoom)

if __name__== "__main__":
    #res = take_picture(URL, "file.jpg")
    #print (res)
    take_serie('tmp',8, 0.8)
