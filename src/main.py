from project_x import project_x
from threading import Thread
import sys

if __name__ == "__main__":
    obj = project_x()
    p1 = Thread()
    if len(sys.argv) == 1:
        p1 = Thread(target=obj.readVideo, args=(0, ))
    else:
        p1 = Thread(target=obj.readVideo, args=(sys.argv[1], ))
    
    p2 = Thread(target=obj.getPoints)
    p3 = Thread(target=obj.recognizeAct)
    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
