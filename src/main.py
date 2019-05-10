from project_x import project_x
from multiprocessing import Process
import sys

if __name__ == "__main__":
    obj = project_x()
    p1 = Process()
    if len(sys.argv) == 1:
        p1 = Process(target=obj.readVideo, args=(0, ))
        p1.start()
    else:
        p1 = Process(target=obj.readVideo, args=(sys.argv[1], ))
        p1.start()
    
    p2 = Process(target=obj.getPoints)
    p2.start()
    p3 = Process(target=obj.recognizeAct)  
    p3.start()

    p1.join()
    p2.join()
    p3.join()
