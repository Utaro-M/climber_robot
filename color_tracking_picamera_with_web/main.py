import time
import threading
import joycon
import color_tracking
import camera

def main():
    thread1 = threading.Thread(target=joycon.joycon_waiting)
    thread2 = threading.Thread(target=color_tracking.color)
    thread3 = threading.Thread(target=camera.show)
    thread1.start()
    thread2.start()
    thread3.start()
    # thread1.join()
    # thread2.join()
