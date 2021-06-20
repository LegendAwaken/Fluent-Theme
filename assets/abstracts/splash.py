from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtCore import *  # pip install PyQt5
from PyQt5.QtGui import *
from win32api import GetSystemMetrics, GetUserName
from threading import Timer
from socket import create_connection
from pyautogui import screenshot
from PyQt5.QtWidgets import *
import sys
from random import randint
from PIL import Image  # pip install pillow
from PIL.ImageFilter import *
import pygetwindow

WIDTH_ = GetSystemMetrics(0)
HEIGHT_ = GetSystemMetrics(1)

class Splash(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(int(WIDTH_ / 1.7), int(HEIGHT_ / 1.9))
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(True)

        self.ui = uic.loadUi("D:/file_explorer_ui/splash.ui", self)
        self.show()
        # self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Splash')

        get_image = screenshot()
        print('Using Brush..')

        # random value grabber
        r = str(randint(10, 100000))

        with open('splash.tru', 'w') as writer:
            writer.write(r)

        # save at this location thi
        get_image.save(f'C:/Users/{GetUserName()}/AppData/Local/Temp/CachedData/cache/vis_ref{r}.jpeg')

        frame_one_image = Image.open(f'C:/Users/{GetUserName()}/AppData/Local/Temp/CachedData/cache/vis_ref{r}.jpeg')

        # blur the image
        skinned = Image.eval(frame_one_image, lambda x: x/1.4)

        frame_one_blurred_image = skinned.filter(GaussianBlur(radius=30))
        frame_one_blurred_image.save(f"C:/Users/{GetUserName()}/AppData/Local/Temp/CachedData/cache/vis_reb1{r}.jpeg")

        self.acrylic.setStyleSheet(f"""
                        background: transparent;
                        background: url('C:/Users/{GetUserName()}/AppData/Local/Temp/CachedData/cache/vis_reb1{r}.jpeg');
                        background-repeat: no-repeat;
                        background-position: center;
                        border: 0;
""")
# #
USER = GetUserName()
# @ staticmethod
def check_window():
    try:
        # get the current active window
        a = pygetwindow.getActiveWindowTitle()

        if str(a) != "Splash":
            try:
                # minimize
                SplashWindow.showMinimized()

                get_image = screenshot()

                # random value grabber
                r = str(randint(10, 100000))

                # save value into a file for furure use   this is the fool
                with open("splash.tru", 'w') as hold:
                    hold.write(r)

                # save at this location thi
                get_image.save(f'C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_ref{r}.jpeg')

                with open("splash.tru", 'r') as val:
                    r = val.read()
                # Frame One UI
                frame_one_image = Image.open(f'C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_ref{r}.jpeg')


                skinned_ = Image.eval(frame_one_image, lambda x: x/1.4)
                # blur the image

                frame_one_blurred_image = skinned_.filter(GaussianBlur(radius=35))
                frame_one_blurred_image.save(f"C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_reb1{r}.jpeg")

                SplashWindow.acrylic.setStyleSheet(f"""
                                background: transparent;
                                background: url('C:/Users/{GetUserName()}/AppData/Local/Temp/CachedData/cache/vis_reb1{r}.jpeg');
                                background-repeat: no-repeat;
                                background-position: center;
                                border: 0;
                                            """)
            # will raise OS error if imaghow to add padding in pushbutton icon in pyqte is subjected to modifications
            except OSError:
                pass

        else:
            pass

    except NameError:
        pass

#
app = QApplication(sys.argv)
SplashWindow = Splash()
# windowTimer = QTimer()
# windowTimer.timeout.connect(check_window)
# windowTimer.setInterval(1)
# windowTimer.start()
SplashWindow.show()


def stop_splash():
    SplashWindow.destroy(destroyWindow=True)
    # app.exit()

def start_splash():
    timer = QTimer()
    timer.timeout.connect(stop_splash)
    timer.setInterval(900)
    timer.start()
    app.exec()


def connection():
    # check internet connection
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        create_connection(("1.1.1.1", 53))
        # change this to true
        return True
    except OSError:
        pass
    return False


