import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from metadataimage import getImageMetaData
from writetodatabase import writeRowToDatabase,deleteFromDatabase
from jsonoperations import readOneJson

def save_time(execution_time):
    file_url = '/home/ubuntu/volume/star_index/tests/write_image_gin.txt'
    with open(file_url, 'a+') as f:
        f.write((str(execution_time)+"\n"))


class Watcher:
    DIRECTORY_TO_WATCH = '/home/ubuntu/volume/star_index/images'

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            print ("received signal. stopping the watch!!")

        self.observer.join()


class Handler(FileSystemEventHandler):
    ''' 
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print ("Received created event - %s." % event.src_path)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print ("Received modified event - %s." % event.src_path)
    '''
    @staticmethod
    def on_created(event):
        path = event.src_path
        start_time = time.time()
        if(path.endswith('.jpg')):
            print("received call on_created %s" % event.src_path)
            tag_dict = getImageMetaData(event.src_path)
    
            if tag_dict == None:
                print("could not write the file %s" % event.src_path)

            else:    
                result = writeRowToDatabase(tag_dict,'image')
                print(result)

        elif(path.endswith('.json')):
            print(".json path path")
            tag_dict = readOneJson(path)
            tag_dict['path'] = path   #specific to the code
            result = writeRowToDatabase(tag_dict,'image')
            execution_time = (time.time() - start_time)*1000
            save_time(execution_time)
            print(result)

        else:
            pass
            


    @staticmethod
    def on_deleted(event):
        print("received call on deleted %s" % event.src_path)
        path = event.src_path
        if '.jpg' not in path:
            pass
        else:
            result = deleteFromDatabase(path, 'image')
            print(result)

    

if __name__ == '__main__':
    w = Watcher()
    w.run()
