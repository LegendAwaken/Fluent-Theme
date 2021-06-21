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
# import keyboard



WIDTH_ = GetSystemMetrics(0)
HEIGHT_ = GetSystemMetrics(1)

class Splash(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(int(WIDTH_ / 1.7), int(HEIGHT_ / 1.9))
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(True)

        # self.ui = uic.loadUi("D:/file_explorer_ui/splash.ui", self)
        # self.show()
        # self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        
        self.setWindowTitle('Splash')

        get_image = screenshot()
        print('Using Brush..')

        # random value grabber
        r = str(randint(10, 100000))

        with open('splash.tru', 'w') as writer:
            writer.write(r)

        # save at this location thi
        get_image.save(f'C:/Users/{GetUserName()}/AppData/Local/Temp/vis_ref{r}.jpeg')

        frame_one_image = Image.open(f'C:/Users/{GetUserName()}/AppData/Local/Temp/vis_ref{r}.jpeg')

        # blur the image
        skinned = Image.eval(frame_one_image, lambda x: x/1.4)

        frame_one_blurred_image = skinned.filter(GaussianBlur(radius=30))
        frame_one_blurred_image.save(f"C:/Users/{GetUserName()}/AppData/Local/Temp/vis_reb1{r}.jpeg")

        self.acrylic.setStyleSheet(f"""
                background: transparent;
                background: url('C:/Users/{GetUserName()}/AppData/Local/Temp/vis_reb1{r}.jpeg');
                background-repeat: no-repeat;
                background-position: center;
                border: 0;
                """)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(706, 440)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.acrylic = QtWidgets.QFrame(Form)
        self.acrylic.setStyleSheet("background: black;\n"
    "border-radius: 50px;")
        self.acrylic.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.acrylic.setFrameShadow(QtWidgets.QFrame.Raised)
        self.acrylic.setObjectName("acrylic")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.acrylic)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self.acrylic)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("text-align: left;\n"
    "background: transparent;\n"
    "color: white;")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/Logician/Downloads/kisspng-apple-worldwide-developers-conference-ios-11-app-s-5b11dda2918327.137142021527897506596.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(120, 120))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton, 0, QtCore.Qt.AlignHCenter)
        self.label = QtWidgets.QLabel(self.acrylic)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setMaximumSize(QtCore.QSize(90, 80))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setStyleSheet("color: white;\n"
    "background: transparent;")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout.addWidget(self.acrylic, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", " Fluent Explorer | 2020.1"))
        self.label.setText(_translate("Form", "Initialising.."))

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
                get_image.save(f'C:/Users/{USER}/AppData/Local/Temp/vis_ref{r}.jpeg')

                with open("splash.tru", 'r') as val:
                    r = val.read()
                # Frame One UI
                frame_one_image = Image.open(f'C:/Users/{USER}/AppData/Local/Temp/vis_ref{r}.jpeg')


                skinned_ = Image.eval(frame_one_image, lambda x: x/1.4)
                # blur the image

                frame_one_blurred_image = skinned_.filter(GaussianBlur(radius=35))
                frame_one_blurred_image.save(f"C:/Users/{USER}/AppData/Local/Temp/vis_reb1{r}.jpeg")

                SplashWindow.acrylic.setStyleSheet(f"""
                                background: transparent;
                                background: url('C:/Users/{GetUserName()}/AppData/Local/Temp/vis_reb1{r}.jpeg');
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


# def mouse_grabber():
#     height = GetSystemMetrics(1)
#     with open('meta.dll', 'w') as writer:
#         if keyboard.mouse.get_position()[1] / height > 0.95:
#             writer.write('True')
#             print('You into taskbar')
#         else:
#             writer.write('False')

def start_splash():
    timer = QTimer()
    timer.timeout.connect(stop_splash)
    # timer.timeout.connect(mouse_grabber)
    timer.setInterval(300)
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


