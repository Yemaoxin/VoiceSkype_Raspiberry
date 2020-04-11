# encoding:utf-8
import multiprocessing
import time
import os


def inputq(queue):
    info = str(+os.getpid()) + ' put : ' + str(time.ctime())
    queue.put(info)
    time.sleep(2)
    info = queue.get()
    print(info)


def outputq(queue):
    info = queue.get()
    print(info)
    queue.put(str(time.ctime()))

if  __name__=="__main__":
    import vlc
    queue = multiprocessing.Queue(10)
    p1 = multiprocessing.Process(target=inputq, args=(queue,))
    p2 = multiprocessing.Process(target=outputq, args=(queue,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()