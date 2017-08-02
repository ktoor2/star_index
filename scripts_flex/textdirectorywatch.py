import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from topicextraction import getTextMetadata
from writetodatabase import writeRowToDatabase,deleteFromDatabase
from jsonoperations import readOneJson
import csv

time_list = []

def save_time(execution_time):

    file_url = '/home/ubuntu/volume/star_index/tests/write_text_update.txt'
    with open(file_url, 'a+') as f:
        f.write((str(execution_time)+"\n"))
        



class Watcher:
    DIRECTORY_TO_WATCH = '/home/ubuntu/volume/star_index/text'

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(10)
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
    def save_time(self, time_list):
        file_url = '/Users/okt/Desktop/my_project/tests/write_text.txt'
        with open(file_url, 'a+') as f:
            wr = csv.writer(f,quoting=csv.QUOTE_ALL)
            wr.writerow(time_list)

    @staticmethod
    def on_created(event):
        print("received call on_created %s" % event.src_path)
        tag_dict = 0
        path = event.src_path
        start_time = time.time()
        if( path.endswith('.txt')):
            print("in txt path")
            tag_dict = getTextMetadata(path)
            print(tag_dict)
        
        elif(path.endswith('.json')):
            print(".json path path")
            tag_dict = readOneJson(path)
            tag_dict['path'] = path   #specific to the code
            print(tag_dict)

        else:
            pass
        

        if tag_dict == None:
            print("could not write the file %s" % event.src_path)

        
        if(tag_dict!=0) :
     
            result = writeRowToDatabase(tag_dict,'text')
            execution_time = (time.time() - start_time)*1000
            print(execution_time)
            save_time(execution_time)
        
        

    @staticmethod
    def on_deleted(event):
        print("received call on deleted %s" % event.src_path)
        path = event.src_path
        if '.txt' not in path or '.json' not in path:
            pass

        else:
            print("starting to delete")
            start_time = time.time()
            result = deleteFromDatabase(path, 'text')
            execution_time = (time.time() - start_time)*1000
            print(execution_time)
            print(result)


    

if __name__ == '__main__':
    w = Watcher()
    w.run()


