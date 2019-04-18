import time
import requests
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import cv2
import json
import time
import base64

class Watcher:
    DIRECTORY_TO_WATCH = "./opgs"

    def __init__(self):
        self.observer = Observer()
    
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")
        self.observer.join()

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            # take any action here when a file is created
            print('Received created event - %s.' % event.src_path)
            addr = 'http://127.0.0.1:5000'
            # prepare headers for http request
            content_type = 'application/json'
            headers = {
                'content-type': content_type
            }
            cur_dir = os.path.dirname(os.path.realpath(__file__))
            img_file = event.src_path.split('\\')[1]
            img_path = cur_dir + '\\opgs\\' + img_file
            img_path = img_path.replace('\\', '/')
            print(img_path)
            time.sleep(1)
            img = cv2.imread(img_path)
            # convert image to string to send it over post request
            with open(img_path, 'rb') as imagefile:
                img_str = base64.b64encode(imagefile.read())
                img_str = img_str.decode('utf-8')
            # send http post request
            data = {
                'image': img_str,
                'filename': event.src_path.split('\\')[1]
            }
            res = requests.post(addr, data = json.dumps(data), headers = headers)
            print(json.loads(res.text))
        elif event.event_type == 'modified':
            # take any action here when a file is modified
            print('Received modified event - %s.' % event.src_path)

if __name__ == '__main__':
    w = Watcher()
    w.run()
    

    
