from config import *

# WARNING: install by pip
USE_PIL = True
try:
    from PIL import Image, ImageTk
except:
    USE_PIL = False
    print('WARNING: Install pillow to enable icon.')


import urllib.request
import os
if not os.path.exists(GAMES_JSON_FILE):
    req = urllib.request.Request(GAMES_JSON_URL)
    print(f'Downloading {GAMES_JSON_FILE}...')
    with urllib.request.urlopen(req) as s:
        content = s.read()
        with open(GAMES_JSON_FILE, 'wb') as f:
            f.write(content)
    if not os.path.exists(GAMES_JSON_FILE):
        print(f'Failed to download {GAMES_JSON_URL} to {GAMES_JSON_FILE}')
        exit()
    print('Downloaded.')


import http.server
import socketserver
import threading
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        p = FLASH_DIR + path
        return super().translate_path(p)

httpd = socketserver.TCPServer(("127.0.0.1", 80), MyHandler)
httpd.timeout = SERVER_TIMEOUT
server_running = True
def server_func():
    while server_running:
        httpd.handle_request()

server_thread = threading.Thread(target=server_func)
print('Starting Server...')
server_thread.start()
print('Started Server')


import tkinter

root = tkinter.Tk()
root.title('Nitrome Game Local Selector')


import json
with open('games.json','r') as f:
    game_list = json.load(f)


game_dict = {dic['name'] : dic for dic in game_list}


label = tkinter.Label(root, text='Nitrome Game Local Selector')
label.pack()

lb = tkinter.Listbox(root, width=40, height=15)
lb.pack()

for game in game_dict:
    lb.insert(tkinter.END, game)

if USE_PIL:
    im = tkinter.Label(root)
    im.pack()
    image = None


from pathlib import Path
def file_name(url):
    fp = Path(url)
    return fp.name


import subprocess
#import os
def select_handler(event):
    idx = lb.curselection()[0]
    game = lb.get(idx)
    print('choose: ', game)
    dic = game_dict[game]
    fname = file_name(dic['url'])
    fpath = FLASH_ROOT + fname
    script = f'\"{FLASH_EXE}\" {fpath}'
    print(script)
    proc = subprocess.Popen(script, start_new_session=True)
    #proc.detach()

lb.bind("<Double-Button-1>", select_handler)

def view_handler(event):
    global image # Memory Management
    idx = lb.curselection()[0]
    game = lb.get(idx)
    print('view: ', game)
    image_path = os.path.join(IMAGE_DIR, game_dict[game]['img'])
    pil_image = Image.open(image_path)
    image = ImageTk.PhotoImage(pil_image)
    print(image_path)
    im.config(image=image)

if USE_PIL:
    lb.bind('<<ListboxSelect>>', view_handler)

#root.geometry('500x300')
root.mainloop()

server_running = False
#httpd.shutdown()
