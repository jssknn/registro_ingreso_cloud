from threading import Event
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import boto3
import os

class Watcher:
    DIRECTORY_TO_WATCH = "C:/fotos/"

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
    S3_BUCKET = "diplocd"
    def on_created(self, event):
        init_size = -1
        while True:
            current_size = os.path.getsize(event.src_path)
            if current_size == init_size:
                break
            else:
                init_size = os.path.getsize(event.src_path)
                time.sleep(2)
        s3 = boto3.client('s3')
        listaArchivo = event.src_path.split('/')
        s3.upload_file(event.src_path,self.S3_BUCKET, listaArchivo[-1])
        print("file copy has now finished", listaArchivo[-1])
            
if __name__ == '__main__':
    w = Watcher()
    w.run()