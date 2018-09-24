import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from subprocess import call
from time import sleep
from sentiment import relativepath
from savetodropbox import absolutebackup
import os

class Watcher:
    DIRECTORY_TO_WATCH=relativepath("")

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
            print ("Error")

        self.observer.join()


class Handler(PatternMatchingEventHandler):
    currentEvent = ""
    update=False
    def __init__(self):
        super(Handler, self).__init__(ignore_directories=True, ignore_patterns=[val for sublist in [[os.path.join(i[0], j) for j in i[2]] for i in os.walk('./.git')] for val in sublist]+['.DS_Store'])
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
        # Take any action here when a file is first created.
            print ("Received event - %s." % event.src_path)
                        
            fpath=str(event.src_path).split('\\')
            directory=str(relativepath('')).split('\\')
            for i in range(len(directory)-1):
                if(fpath[0]==directory[0]):
                    fpath.pop(0)
                    directory.pop(0)
            path=str.join('/',fpath)
            #print(path)
            #call(['python','savetodropbox.py',path] , shell=True)
            absolutebackup(path)

            sleep(30)
        elif event.event_type == 'modified':
        # Taken any action here when a file is modified.
            print ("Received event - %s." % event.src_path)
                             
            fpath=str(event.src_path).split('\\')
            directory=str(relativepath('')).split('\\')
            for i in range(len(directory)-1):
                if(fpath[0]==directory[0]):
                    fpath.pop(0)
                    directory.pop(0)
            path=str.join('/',fpath)
            call(['python','savetodropbox.py',path] , shell=True)
            #print(path)
            absolutebackup(path)
            sleep(30)



if __name__ == '__main__':
    w = Watcher()
    w.run()
