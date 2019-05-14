"""python + opencv 实现屏幕录制_by-_Zjh_"""
from PIL import ImageGrab
import numpy as np
import cv2
import threading
from time import sleep
import shutil


class Job(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # super(Job, self).__init__(*args, **kwargs)
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()  # 将running设置为True

    def run(self):
        p = ImageGrab.grab()  # 获得当前屏幕
        # k = np.zeros((200, 200), np.uint8)
        a, b = p.size  # 获得当前屏幕的大小
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 编码格式
        video = cv2.VideoWriter('test.avi', fourcc, 16,
                                (a, b))  # 输出文件命名为test.mp4,帧率为16，可以自己设置
        while self.__running.is_set():
            im = ImageGrab.grab()
            imm = cv2.cvtColor(np.array(im),
                               cv2.COLOR_RGB2BGR)  # 转为opencv的BGR格式
            video.write(imm)
            # cv2.imshow('imm', k)
            cv2.waitKey(1)
        video.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.__running.clear()  # 设置为False


if __name__ == '__main__':

    Save = Job()
    Save.start()
    sleep(5)
    Save.stop()
    sleep(1)

    shutil.move('test.avi',
                'test1.avi')
