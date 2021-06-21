from threading import Thread

from PyQt5.QtWebEngineWidgets import *  # search for it
from pyautogui import *
from win32api import *
from win10toast import ToastNotifier
import keyboard
from pygame import mixer, error, USEREVENT, event
from mutagen.mp3 import MP3, HeaderNotFoundError, MutagenError
from assets.abstracts.splash import *
from random import choice

# constants
WIDTH_ = GetSystemMetrics(0)
HEIGHT_ = GetSystemMetrics(1)
USER = GetUserName()
PATH_ = ""
# may be i not pretty
if not os.path.isdir(f'C:/Users/{USER}/AppData/Local/Temp/CachedData/cache'):
    os.makedirs(f'C:/Users/{USER}/AppData/Local/Temp/CachedData/cache')


class BlurEffect(QtWidgets.QGraphicsBlurEffect):
    effectRect = None

    def setEffectRect(self, rect):
        self.effectRect = rect
        self.update()

    def draw(self, qp):
        if self.effectRect is None or self.effectRect.isNull():
            # no valid effect rect to be used, use the default implementation
            super().draw(qp)

        else:
            qp.save()
            # clip the drawing so that it's restricted to the effectRect
            qp.setClipRect(self.effectRect)
            # call the default implementation, which will draw the effect
            super().draw(qp)
            # get the full region that should be painted
            fullRegion = QtGui.QRegion(qp.viewport())
            # and subtract the effect rectangle
            fullRegion -= QtGui.QRegion(self.effectRect)
            qp.setClipRegion(fullRegion)
            # draw the *source*, which has no effect applied
            self.drawSource(qp)
            qp.restore()


class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.value = False
        self.setMinimumSize(int(WIDTH_ / 1.2), int(HEIGHT_ / 1.2))
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(True)
        self.username = GetUserName()

        # # # UI Setup
        # self.ui = uic.loadUi("D:/file_explorer_ui/UPDATE4.ui", self)
        # self.show()
        self.setupUi(self)

        # Visibility
        self.sent_ui.setVisible(False)
        self.send_feedback.setVisible(False)
        self.write_to_us_box.setEnabled(False)
        self.response.setVisible(False)

        # self.sent_ui.setVisible(False)
        # self.write_to_us_box.setVisible(False)
        # radio button manager
        with open("lib.dll", "r") as reader:
            read = str(reader.read())

        # combobox manager
        with open('rep32.dll', 'r') as theme_reader:
            read_theme = theme_reader.read()

        if read == "True":
            self.effect_radiobutton.setChecked(True)
            self.set_acrylic(True, "set_all")
        else:
            self.effect_radiobutton.setChecked(False)
            self.set_acrylic(False, "dark")
            print('dark')

        # additional settigs

        if read_theme == 'acrylic':
            self.theme_box.setCurrentIndex(1)
            self.additional_settings_manager('set_invisible')
        elif read_theme == 'transparent':
            self.theme_box.setCurrentIndex(2)
            self.additional_settings_manager('tint_only')
        elif read_theme == 'blur':
            self.theme_box.setCurrentIndex(3)
            self.additional_settings_manager('set_visible')
        elif read_theme == 'light':
            self.theme_box.setCurrentIndex(4)
        elif read_theme == 'dark':
            self.theme_box.setCurrentIndex(5)
            self.additional_settings_manager('set_invisible')
        elif read_theme == 'amoled':
            self.theme_box.setCurrentIndex(6)
        elif read_theme == 'default':
            self.theme_box.setCurrentIndex(0)
        # self.setupUi(self)
        self.functionalities()
        self.setGeometry(int(WIDTH_ / 12), int(HEIGHT_ / 16), int(WIDTH_ / 1.14), int(HEIGHT_ / 1.19))
        self.showMaximized()

        with open("config.dll", "r") as reader:
            read_config = reader.read()

        # grab screen
        if read_config == "True" or read_config == '':
            get_image = screenshot()
            print('Using Brush..')

            # random value grabber
            r = str(randint(10, 100000))

            # save value into a file for furure use   this is the fool
            with open("assets/resources/holder.tru", 'w') as hold:
                hold.write(r)

            # save at this location thi
            get_image.save(f'C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_ref{r}.jpeg')

        with open("assets/resources/holder.tru", 'r') as val:
            r = val.read()
        # Frame One UI
        frame_one_image = Image.open(f'C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_ref{r}.jpeg')

        with open('effectSupport.dll', 'r') as reader:
            read = reader.read()

        if read == 'ten':
            func = lambda x: x / 2.2
        else:
            func = lambda x: x / 3.5

        skinned_ = Image.eval(frame_one_image, func)
        # blur the image

        if read == 'ten':
            radii = 10
        else:
            radii = 35

        frame_one_blurred_image = skinned_.filter(GaussianBlur(radius=radii))
        frame_one_blurred_image.save(f"C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_reb1{r}.jpeg")

        self.setTheme()
        self.temp_checksum()


    #     self.mainlayout = QtWidgets.QVBoxLayout(self)
    #     self.mainlayout.setContentsMargins(0, 0, 0, 0)
    #
    #     self.subWidget = QtWidgets.QWidget()
    #     self.mainlayout.addWidget(self.subWidget)
    #
    #     self.effect = BlurEffect()
    #
    #     self.subWidget.setGraphicsEffect(self.effect)
    #     self.effect.setEnabled(True)
    #     self.effect.setBlurRadius(40)
    #
    #     self.menu = QtWidgets.QWidget(self)
    #     self.menu.setVisible(False)
    #     self.menu.setFixedWidth(300)
    #     self.menu.move(-self.menu.width(), 0)
    #
    #     self.menuLayout = QtWidgets.QVBoxLayout(self.menu)
    #
    #     self.menuAnimation = QtCore.QVariantAnimation()
    #     self.menuAnimation.setDuration(400)
    #     self.menuAnimation.setEasingCurve(QtCore.QEasingCurve.OutQuart)
    #     self.menuAnimation.setStartValue(-self.menu.width())
    #     self.menuAnimation.setEndValue(0)
    #
    #
    # def openMenu(self):
    #     # if self.menu.x() >= 0:
    #     #     # the menu is already visible
    #     #     return
    #     # ensure that the menu starts hidden (that is, with its right border
    #     # aligned to the left of the main widget)
    #     self.menu.move(-self.menu.width(), 0)
    #     self.menu.setVisible(True)
    #     self.menu.setFocus()
    #
    #     # enable the effect, set the forward direction for the animation, and
    #     # start it; it's important to set the effect rectangle here too, otherwise
    #     # some flickering might show at the beginning
    #     self.effect.setEffectRect(self.menu.geometry())
    #     self.effect.setEnabled(True)
    #     self.menuAnimation.setDirection(QtCore.QVariantAnimation.Forward)
    #     self.menuAnimation.start()
    #     print("Trying ..")
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(979, 761)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.all_frame = QtWidgets.QFrame(Form)
        self.all_frame.setObjectName("all_frame")
        self.main_layout = QtWidgets.QHBoxLayout(self.all_frame)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setObjectName("main_layout")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.graphics = QtWidgets.QFrame(self.all_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphics.sizePolicy().hasHeightForWidth())
        self.graphics.setSizePolicy(sizePolicy)
        self.graphics.setMinimumSize(QtCore.QSize(350, 0))
        self.graphics.setMaximumSize(QtCore.QSize(380, 771))
        self.graphics.setStyleSheet("background: black;")
        self.graphics.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.graphics.setFrameShadow(QtWidgets.QFrame.Plain)
        self.graphics.setLineWidth(0)
        self.graphics.setObjectName("graphics")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.graphics)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(10, 4, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.collapse = QtWidgets.QPushButton(self.graphics)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.collapse.sizePolicy().hasHeightForWidth())
        self.collapse.setSizePolicy(sizePolicy)
        self.collapse.setMinimumSize(QtCore.QSize(20, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.collapse.setFont(font)
        self.collapse.setStyleSheet("QPushButton{\n"
                                    "color: white;\n"
                                    "background: transparent;\n"
                                    "text-align: left;\n"
                                    "padding-left: 4px;\n"
                                    "\n"
                                    "\n"
                                    "}\n"
                                    "\n"
                                    "\n"
                                    "QPushButton::pressed{\n"
                                    "    background-color: rgba(255, 255, 255, 30)\n"
                                    "}\n"
                                    "")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/resources/images/menu.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.collapse.setIcon(icon)
        self.collapse.setAutoRepeat(True)
        self.collapse.setObjectName("collapse")
        self.horizontalLayout_4.addWidget(self.collapse, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(7, -1, 17, -1)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.search = QtWidgets.QPushButton(self.graphics)
        self.search.setMinimumSize(QtCore.QSize(40, 45))
        self.search.setMaximumSize(QtCore.QSize(200, 16777215))
        self.search.setStyleSheet("background: transparent;")
        self.search.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("assets/resources/images/icons8-search-30.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.search.setIcon(icon1)
        self.search.setIconSize(QtCore.QSize(20, 20))
        self.search.setObjectName("search")
        self.horizontalLayout.addWidget(self.search)
        self.search_box = QtWidgets.QLineEdit(self.graphics)
        self.search_box.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.search_box.setFont(font)
        self.search_box.setStyleSheet("QLineEdit {\n"
                                      "    color: white;\n"
                                      "   border-radius: 5px;\n"
                                      "  border: 2px solid rgb(91, 101, 124);\n"
                                      "   padding-left: 10px;\n"
                                      "   selection-color: rgb(255, 255, 255);\n"
                                      "   selection-background-color: rgb(255, 121, 198);\n"
                                      "    background: transparent;\n"
                                      "}\n"
                                      "\n"
                                      "QLineEdit:hover {\n"
                                      "   border: 2px solid rgb(64, 71, 88);\n"
                                      "    background-color: rgba(255, 255, 255, 30)\n"
                                      "}\n"
                                      "\n"
                                      "QLineEdit:focus {\n"
                                      "  border: 2px solid rgb(91, 101, 124);\n"
                                      "}")
        self.search_box.setObjectName("search_box")
        self.horizontalLayout.addWidget(self.search_box)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem2)
        self.GDrive = QtWidgets.QPushButton(self.graphics)
        self.GDrive.setMinimumSize(QtCore.QSize(0, 45))
        self.GDrive.setMaximumSize(QtCore.QSize(420, 45))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.GDrive.setFont(font)
        self.GDrive.setAutoFillBackground(False)
        self.GDrive.setStyleSheet("QPushButton{\n"
                                  "color: white;\n"
                                  "background: transparent;\n"
                                  "text-align: left;    \n"
                                  "padding-left: 10px;\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton::hover{\n"
                                  "    color: white;\n"
                                  "    background-color : rgba(255, 255  ,255 ,50);\n"
                                  "\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton::pressed{\n"
                                  "    background-color: rgba(255, 255, 255, 80)\n"
                                  "}\n"
                                  "\n"
                                  "QTabBar::tab::disabled {width: 0; height: 0; margin: 0; padding: 0; border: none;} ")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("assets/resources/images/icons8-google-drive-25.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.GDrive.setIcon(icon2)
        self.GDrive.setIconSize(QtCore.QSize(25, 25))
        self.GDrive.setObjectName("GDrive")
        self.verticalLayout_3.addWidget(self.GDrive)
        self.gdrive_line = QtWidgets.QFrame(self.graphics)
        self.gdrive_line.setMaximumSize(QtCore.QSize(16777215, 1))
        self.gdrive_line.setStyleSheet("background-color: rgba(255, 255, 255, 80);\n"
                                       "color: rgba(255, 255, 255, 80);\n"
                                       "margin-left: 15px;\n"
                                       "margin-right: 25px;")
        self.gdrive_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.gdrive_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gdrive_line.setObjectName("gdrive_line")
        self.verticalLayout_3.addWidget(self.gdrive_line)
        self.thisPC = QtWidgets.QPushButton(self.graphics)
        self.thisPC.setMinimumSize(QtCore.QSize(0, 45))
        self.thisPC.setMaximumSize(QtCore.QSize(420, 45))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.thisPC.setFont(font)
        self.thisPC.setStyleSheet("QPushButton{\n"
                                  "color: white;\n"
                                  "background: transparent;\n"
                                  "text-align: left;    \n"
                                  "padding-left: 10px;\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton::hover{\n"
                                  "    color: white;\n"
                                  "    background-color : rgba(255, 255  ,255 ,50);\n"
                                  "\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton::pressed{\n"
                                  "    background-color: rgba(255, 255, 255, 80)\n"
                                  "}\n"
                                  "")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("assets/resources/images/icons8-laptop-computer-25.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.thisPC.setIcon(icon3)
        self.thisPC.setIconSize(QtCore.QSize(25, 25))
        self.thisPC.setObjectName("thisPC")
        self.verticalLayout_3.addWidget(self.thisPC)
        self.downloads = QtWidgets.QPushButton(self.graphics)
        self.downloads.setMinimumSize(QtCore.QSize(0, 45))
        self.downloads.setMaximumSize(QtCore.QSize(420, 45))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.downloads.setFont(font)
        self.downloads.setStyleSheet("QPushButton{\n"
                                     "color: white;\n"
                                     "background: transparent;\n"
                                     "text-align: left;    \n"
                                     "padding-left: 10px;\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton::hover{\n"
                                     "    color: white;\n"
                                     "    background-color : rgba(255, 255  ,255 ,50);\n"
                                     "\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton::pressed{\n"
                                     "    background-color: rgba(255, 255, 255, 80)\n"
                                     "}\n"
                                     "")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("assets/resources/images/icons8-downloads-folder-25.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.downloads.setIcon(icon4)
        self.downloads.setIconSize(QtCore.QSize(25, 25))
        self.downloads.setObjectName("downloads")
        self.verticalLayout_3.addWidget(self.downloads)
        self.pictures = QtWidgets.QPushButton(self.graphics)
        self.pictures.setMinimumSize(QtCore.QSize(0, 45))
        self.pictures.setMaximumSize(QtCore.QSize(420, 45))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pictures.setFont(font)
        self.pictures.setStyleSheet("QPushButton{\n"
                                    "color: white;\n"
                                    "background: transparent;\n"
                                    "text-align: left;    \n"
                                    "padding-left: 10px;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton::hover{\n"
                                    "    color: white;\n"
                                    "    background-color : rgba(255, 255  ,255 ,50);\n"
                                    "\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton::pressed{\n"
                                    "    background-color: rgba(255, 255, 255, 80)\n"
                                    "}\n"
                                    "")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("assets/resources/images/picture25.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.pictures.setIcon(icon5)
        self.pictures.setIconSize(QtCore.QSize(25, 25))
        self.pictures.setObjectName("pictures")
        self.verticalLayout_3.addWidget(self.pictures)
        self.videos = QtWidgets.QPushButton(self.graphics)
        self.videos.setMinimumSize(QtCore.QSize(0, 45))
        self.videos.setMaximumSize(QtCore.QSize(420, 45))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.videos.setFont(font)
        self.videos.setStyleSheet("QPushButton{\n"
                                  "color: white;\n"
                                  "background: transparent;\n"
                                  "text-align: left;    \n"
                                  "padding-left: 10px;\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton::hover{\n"
                                  "    color: white;\n"
                                  "    background-color : rgba(255, 255  ,255 ,50);\n"
                                  "\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton::pressed{\n"
                                  "    background-color: rgba(255, 255, 255, 80)\n"
                                  "}\n"
                                  "")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("assets/resources/images/movie25.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.videos.setIcon(icon6)
        self.videos.setIconSize(QtCore.QSize(34, 34))
        self.videos.setObjectName("videos")
        self.verticalLayout_3.addWidget(self.videos)
        self.music = QtWidgets.QPushButton(self.graphics)
        self.music.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.music.setFont(font)
        self.music.setStyleSheet("QPushButton{\n"
                                 "color: white;\n"
                                 "background: transparent;\n"
                                 "text-align: left;    \n"
                                 "padding-left: 10px;\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton::hover{\n"
                                 "    color: white;\n"
                                 "    background-color : rgba(255, 255  ,255 ,50);\n"
                                 "\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton::pressed{\n"
                                 "    background-color: rgba(255, 255, 255, 80)\n"
                                 "}\n"
                                 "")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("assets/resources/images/music25.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.music.setIcon(icon7)
        self.music.setIconSize(QtCore.QSize(25, 25))
        self.music.setObjectName("music")
        self.verticalLayout_3.addWidget(self.music)
        self.documents = QtWidgets.QPushButton(self.graphics)
        self.documents.setMinimumSize(QtCore.QSize(0, 45))
        self.documents.setMaximumSize(QtCore.QSize(420, 16777215))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.documents.setFont(font)
        self.documents.setStyleSheet("QPushButton{\n"
                                     "color: white;\n"
                                     "background: transparent;\n"
                                     "text-align: left;    \n"
                                     "padding-left: 10px;\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton::hover{\n"
                                     "    color: white;\n"
                                     "    background-color : rgba(255, 255  ,255 ,50);\n"
                                     "\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton::pressed{\n"
                                     "    background-color: rgba(255, 255, 255, 80)\n"
                                     "}\n"
                                     "")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("assets/resources/images/documents25.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.documents.setIcon(icon8)
        self.documents.setIconSize(QtCore.QSize(25, 25))
        self.documents.setObjectName("documents")
        self.verticalLayout_3.addWidget(self.documents)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.settings_line = QtWidgets.QFrame(self.graphics)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settings_line.sizePolicy().hasHeightForWidth())
        self.settings_line.setSizePolicy(sizePolicy)
        self.settings_line.setMinimumSize(QtCore.QSize(378, 1))
        self.settings_line.setMaximumSize(QtCore.QSize(16777215, 0))
        self.settings_line.setStyleSheet("background-color: rgba(255, 255, 255, 80);\n"
                                         "color: rgba(255, 255, 255, 80);\n"
                                         "margin-left: 15px;\n"
                                         "margin-right: 25px;")
        self.settings_line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.settings_line.setLineWidth(1)
        self.settings_line.setMidLineWidth(1)
        self.settings_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.settings_line.setObjectName("settings_line")
        self.verticalLayout_3.addWidget(self.settings_line, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.settings = QtWidgets.QPushButton(self.graphics)
        self.settings.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.settings.setFont(font)
        self.settings.setStyleSheet("QPushButton{\n"
                                    "color: white;\n"
                                    "background: transparent;\n"
                                    "text-align: left;    \n"
                                    "padding-left: 10px;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton::hover{\n"
                                    "    color: white;\n"
                                    "    background-color : rgba(255, 255  ,255 ,50);\n"
                                    "\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton::pressed{\n"
                                    "    background-color: rgba(255, 255, 255, 80)\n"
                                    "}\n"
                                    "")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("assets/resources/images/icons8-window-settings-25.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.settings.setIcon(icon9)
        self.settings.setIconSize(QtCore.QSize(34, 34))
        self.settings.setObjectName("settings")
        self.verticalLayout_3.addWidget(self.settings)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.gridLayout_5.addWidget(self.graphics, 0, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.all_frame)
        self.line_2.setMaximumSize(QtCore.QSize(1, 16777215))
        self.line_2.setStyleSheet("background-color:  rgba(255, 255, 255, 30);\n"
                                  "color: rgba(255, 255, 255, 30);\n"
                                  "margin-left: 15px;\n"
                                  "margin-right: 15px;")
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_5.addWidget(self.line_2, 0, 1, 1, 1)
        self.main_layout.addLayout(self.gridLayout_5)
        self.window_frame = QtWidgets.QFrame(self.all_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.window_frame.sizePolicy().hasHeightForWidth())
        self.window_frame.setSizePolicy(sizePolicy)
        self.window_frame.setStyleSheet("background: rgba(0, 0, 0, 60);")
        self.window_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.window_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.window_frame.setLineWidth(0)
        self.window_frame.setObjectName("window_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.window_frame)
        self.verticalLayout.setContentsMargins(-1, -1, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButton = QtWidgets.QPushButton(self.window_frame)
        self.pushButton.setStyleSheet("background: transparent;")
        self.pushButton.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("assets/resources/images/icons8-back-25.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.pushButton.setIcon(icon10)
        self.pushButton.setIconSize(QtCore.QSize(30, 25))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_5.addWidget(self.pushButton)
        self.pushButton_4 = QtWidgets.QPushButton(self.window_frame)
        self.pushButton_4.setStyleSheet("background: transparent;")
        self.pushButton_4.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("assets/resources/images/icons8-forward-25.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        icon11.addPixmap(QtGui.QPixmap("assets/resources/images/icons8-forward-25 (1).png"), QtGui.QIcon.Disabled,
                         QtGui.QIcon.On)
        self.pushButton_4.setIcon(icon11)
        self.pushButton_4.setIconSize(QtCore.QSize(30, 20))
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_5.addWidget(self.pushButton_4)
        self.line_3 = QtWidgets.QFrame(self.window_frame)
        self.line_3.setMaximumSize(QtCore.QSize(1, 16777215))
        self.line_3.setStyleSheet("background-color: rgba(255, 255, 255, 80);\n"
                                  "color: rgba(255, 255, 255, 80);\n"
                                  "margin-left: 15px;\n"
                                  "margin-right: 25px;")
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout_5.addWidget(self.line_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.window_frame)
        self.pushButton_2.setStyleSheet("background: transparent;n")
        self.pushButton_2.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("assets/resources/images/icons8-up-arrow-25 (1).png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        icon12.addPixmap(QtGui.QPixmap("assets/resources/images/icons8-up-arrow-25 (2).png"), QtGui.QIcon.Disabled,
                         QtGui.QIcon.On)
        self.pushButton_2.setIcon(icon12)
        self.pushButton_2.setIconSize(QtCore.QSize(30, 18))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_5.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.window_frame)
        self.pushButton_3.setStyleSheet("background: transparent;")
        self.pushButton_3.setText("")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("assets/resources/images/icons8-refresh-30.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        icon13.addPixmap(QtGui.QPixmap("assets/resources/images/icons8-refresh-30 (1).png"), QtGui.QIcon.Disabled,
                         QtGui.QIcon.On)
        self.pushButton_3.setIcon(icon13)
        self.pushButton_3.setIconSize(QtCore.QSize(30, 20))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_5.addWidget(self.pushButton_3)
        self.path = QtWidgets.QLineEdit(self.window_frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.path.setFont(font)
        self.path.setStyleSheet("QLineEdit {\n"
                                "   color: white;\n"
                                "   border-radius: 5px;\n"
                                "   border: 2px solid rgb(91, 101, 124);\n"
                                "   padding-left: 10px;\n"
                                "   selection-color: rgb(255, 255, 255);\n"
                                "   selection-background-color: rgb(255, 121, 198);\n"
                                "   \n"
                                "}\n"
                                "\n"
                                "QLineEdit:hover {\n"
                                "   border: 2px solid rgb(64, 71, 88);\n"
                                "    background-color: rgba(255, 255, 255, 30);\n"
                                "}\n"
                                "\n"
                                "QLineEdit:focus {\n"
                                "  border: 2px solid rgb(91, 101, 124);\n"
                                "}")
        self.path.setText("")
        self.path.setClearButtonEnabled(True)
        self.path.setObjectName("path")
        self.horizontalLayout_5.addWidget(self.path)
        self.minimize = QtWidgets.QPushButton(self.window_frame)
        self.minimize.setStyleSheet("QPushButton{\n"
                                    "color: white;\n"
                                    "background: transparent;\n"
                                    "\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton::hover{\n"
                                    "    color: white;\n"
                                    "    background-color : rgba(255, 255  ,255 ,50);\n"
                                    "    border: 200px;\n"
                                    "    \n"
                                    "}\n"
                                    "\n"
                                    "QPushButton::pressed{\n"
                                    "    background-color: rgba(255, 255, 255, 80)\n"
                                    "}\n"
                                    "")
        self.minimize.setText("")
        icon14 = QtGui.QIcon()
        icon14.addPixmap(
            QtGui.QPixmap("assets/resources/images/minimize.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.minimize.setIcon(icon14)
        self.minimize.setObjectName("minimize")
        self.horizontalLayout_5.addWidget(self.minimize)
        self.maximize = QtWidgets.QPushButton(self.window_frame)
        self.maximize.setStyleSheet("QPushButton{\n"
                                    "color: white;\n"
                                    "background: transparent;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton::hover{\n"
                                    "    color: white;\n"
                                    "    background-color : rgba(255, 255  ,255 ,50);\n"
                                    "\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton::pressed{\n"
                                    "    background-color: rgba(255, 255, 255, 80)\n"
                                    "}\n"
                                    "")
        self.maximize.setText("")
        icon15 = QtGui.QIcon()
        icon15.addPixmap(
            QtGui.QPixmap("assets/resources/images/estore.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.maximize.setIcon(icon15)
        self.maximize.setObjectName("maximize")
        self.horizontalLayout_5.addWidget(self.maximize)
        self.close = QtWidgets.QPushButton(self.window_frame)
        self.close.setStyleSheet("QPushButton{\n"
                                 "color: white;\n"
                                 "background: transparent;\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton::hover{\n"
                                 "    color: white;\n"
                                 "    background-color : rgba(255, 255  ,255 ,50);\n"
                                 "\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton::pressed{\n"
                                 "    background-color: rgba(255, 255, 255, 80)\n"
                                 "}\n"
                                 "")
        self.close.setText("")
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap("assets/resources/images/close.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.close.setIcon(icon16)
        self.close.setObjectName("close")
        self.horizontalLayout_5.addWidget(self.close)
        spacerItem4 = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.main_stacked_widget = QtWidgets.QStackedWidget(self.window_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_stacked_widget.sizePolicy().hasHeightForWidth())
        self.main_stacked_widget.setSizePolicy(sizePolicy)
        self.main_stacked_widget.setStyleSheet("background: transparent;")
        self.main_stacked_widget.setObjectName("main_stacked_widget")
        self.main_pages = QtWidgets.QWidget()
        self.main_pages.setObjectName("main_pages")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.main_pages)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.main_frame = QtWidgets.QFrame(self.main_pages)
        self.main_frame.setStyleSheet("background: transparent;")
        self.main_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.main_frame.setObjectName("main_frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.main_frame)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.main_frame)
        self.tabWidget.setMinimumSize(QtCore.QSize(600, 700))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet("\n"
                                     "QTabBar::tab {\n"
                                     "    background-color: rgba(255, 255, 255, 30);\n"
                                     "    color: white;\n"
                                     "    padding: 8px;\n"
                                     "    border-radius: 7px;\n"
                                     "    margin: 2px;\n"
                                     "}\n"
                                     "\n"
                                     "QTabBar::tab:hover {\n"
                                     "    background-color: rgba(0, 0, 0, 70);\n"
                                     "    color: white;\n"
                                     "    padding: 4px;\n"
                                     "    border-radius: 7px;\n"
                                     "    margin: 2px;\n"
                                     "}\n"
                                     "\n"
                                     "QTabBar::close-button{\n"
                                     "   margin-right: 10px;\n"
                                     "   image: url(\'assets/resources/images/close.png\')\n"
                                     "}\n"
                                     "\n"
                                     "\n"
                                     "")
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(20, 20))
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabBarAutoHide(True)
        self.tabWidget.setObjectName("tabWidget")
        self.this_pc_2 = QtWidgets.QWidget()
        self.this_pc_2.setObjectName("this_pc_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.this_pc_2)
        self.gridLayout_4.setVerticalSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.this_pc_label = QtWidgets.QPushButton(self.this_pc_2)
        self.this_pc_label.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.this_pc_label.setFont(font)
        self.this_pc_label.setStyleSheet("color: white;\n"
                                         "padding-top: 5px;")
        self.this_pc_label.setObjectName("this_pc_label")
        self.gridLayout_4.addWidget(self.this_pc_label, 0, 0, 1, 1)
        self.library_layout = QtWidgets.QGridLayout()
        self.library_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.library_layout.setSpacing(4)
        self.library_layout.setObjectName("library_layout")
        self.gridLayout_4.addLayout(self.library_layout, 4, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_4.addItem(spacerItem5, 2, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem6, 9, 0, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.this_pc_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setStyleSheet(
            "color: white; background: transparent; text-align: left; margin-left: 7px; margin-bottom: 12px; margin-top: 15px;")
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout_4.addWidget(self.pushButton_6, 5, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.this_pc_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet(
            "color: white; background: transparent; text-align: left; margin-left: 7px; margin-bottom: 12px;")
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_4.addWidget(self.pushButton_5, 3, 0, 1, 1)
        self.drives_layout = QtWidgets.QGridLayout()
        self.drives_layout.setObjectName("drives_layout")
        self.gridLayout_4.addLayout(self.drives_layout, 6, 0, 1, 1)
        self.tabWidget.addTab(self.this_pc_2, "")
        self.downloads_tab = QtWidgets.QWidget()
        self.downloads_tab.setObjectName("downloads_tab")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.downloads_tab)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.downloads_frame = QtWidgets.QFrame(self.downloads_tab)
        self.downloads_frame.setMinimumSize(QtCore.QSize(580, 654))
        self.downloads_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.downloads_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.downloads_frame.setObjectName("downloads_frame")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.downloads_frame)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.downloads_label = QtWidgets.QPushButton(self.downloads_frame)
        self.downloads_label.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.downloads_label.setFont(font)
        self.downloads_label.setStyleSheet("color: white;\n"
                                           "padding-top: 5px;")
        self.downloads_label.setObjectName("downloads_label")
        self.verticalLayout_10.addWidget(self.downloads_label)
        self.downloads_layout = QtWidgets.QVBoxLayout()
        self.downloads_layout.setObjectName("downloads_layout")
        self.verticalLayout_10.addLayout(self.downloads_layout)
        self.verticalLayout_5.addWidget(self.downloads_frame)
        self.verticalLayout_7.addLayout(self.verticalLayout_5)
        self.tabWidget.addTab(self.downloads_tab, "")
        self.music_tab = QtWidgets.QWidget()
        self.music_tab.setObjectName("music_tab")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.music_tab)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.music_frame = QtWidgets.QFrame(self.music_tab)
        self.music_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.music_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.music_frame.setObjectName("music_frame")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.music_frame)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.this_pc_label_2 = QtWidgets.QPushButton(self.music_frame)
        self.this_pc_label_2.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.this_pc_label_2.setFont(font)
        self.this_pc_label_2.setStyleSheet("color: white;\n"
                                           "padding-top: 5px;")
        self.this_pc_label_2.setObjectName("this_pc_label_2")
        self.verticalLayout_8.addWidget(self.this_pc_label_2)
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.songs_frane = QtWidgets.QFrame(self.music_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.songs_frane.sizePolicy().hasHeightForWidth())
        self.songs_frane.setSizePolicy(sizePolicy)
        self.songs_frane.setMinimumSize(QtCore.QSize(300, 0))
        self.songs_frane.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.songs_frane.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.songs_frane.setFrameShadow(QtWidgets.QFrame.Raised)
        self.songs_frane.setObjectName("songs_frane")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.songs_frane)
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.songs_layout = QtWidgets.QVBoxLayout()
        self.songs_layout.setObjectName("songs_layout")
        self.songs_scroll = QtWidgets.QScrollBar(self.songs_frane)
        self.songs_scroll.setOrientation(QtCore.Qt.Vertical)
        self.songs_scroll.setObjectName("songs_scroll")
        self.songs_layout.addWidget(self.songs_scroll)
        self.verticalLayout_18.addLayout(self.songs_layout)
        self.verticalLayout_15.addWidget(self.songs_frane)
        self.gridLayout_10.addLayout(self.verticalLayout_15, 0, 0, 1, 1)
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.preview_frame = QtWidgets.QFrame(self.music_frame)
        self.preview_frame.setMinimumSize(QtCore.QSize(200, 0))
        self.preview_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.preview_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.preview_frame.setObjectName("preview_frame")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.preview_frame)
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_20.setSpacing(0)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.preview_layout = QtWidgets.QVBoxLayout()
        self.preview_layout.setObjectName("preview_layout")
        self.verticalLayout_20.addLayout(self.preview_layout)
        self.verticalLayout_16.addWidget(self.preview_frame)
        self.gridLayout_10.addLayout(self.verticalLayout_16, 0, 1, 1, 1)
        self.verticalLayout_8.addLayout(self.gridLayout_10)
        self.verticalLayout_2.addWidget(self.music_frame)
        self.gridLayout_9.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.music_tab, "")
        self.settings1 = QtWidgets.QWidget()
        self.settings1.setObjectName("settings1")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.settings1)
        self.gridLayout_8.setContentsMargins(0, -1, 0, 0)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.settings_3 = QtWidgets.QFrame(self.settings1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settings_3.sizePolicy().hasHeightForWidth())
        self.settings_3.setSizePolicy(sizePolicy)
        self.settings_3.setMinimumSize(QtCore.QSize(240, 0))
        self.settings_3.setStyleSheet("")
        self.settings_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.settings_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.settings_3.setLineWidth(1)
        self.settings_3.setMidLineWidth(1)
        self.settings_3.setObjectName("settings_3")
        self.verticalLayout_23 = QtWidgets.QVBoxLayout(self.settings_3)
        self.verticalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_23.setSpacing(0)
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.verticalLayout_24 = QtWidgets.QVBoxLayout()
        self.verticalLayout_24.setSpacing(0)
        self.verticalLayout_24.setObjectName("verticalLayout_24")
        spacerItem7 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_24.addItem(spacerItem7)
        self.settings_button = QtWidgets.QPushButton(self.settings_3)
        self.settings_button.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.settings_button.setFont(font)
        self.settings_button.setStyleSheet("color: white; background: transparent;")
        icon17 = QtGui.QIcon()
        icon17.addPixmap(
            QtGui.QPixmap("assets/resources/images/settings.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settings_button.setIcon(icon17)
        self.settings_button.setIconSize(QtCore.QSize(45, 45))
        self.settings_button.setCheckable(False)
        self.settings_button.setObjectName("settings_button")
        self.verticalLayout_24.addWidget(self.settings_button)
        spacerItem8 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_24.addItem(spacerItem8)
        self.appearance = QtWidgets.QPushButton(self.settings_3)
        self.appearance.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.appearance.setFont(font)
        self.appearance.setStyleSheet("QPushButton{\n"
                                      "color: white;\n"
                                      "background: transparent;\n"
                                      "padding-left: 10px;\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton::hover{\n"
                                      "    color: white;\n"
                                      "    background-color : rgba(255, 255  ,255 ,50);\n"
                                      "\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton::pressed{\n"
                                      "    background-color: rgba(255, 255, 255, 80)\n"
                                      "}\n"
                                      "")
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap("assets/resources/images/appearance.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.appearance.setIcon(icon18)
        self.appearance.setIconSize(QtCore.QSize(35, 35))
        self.appearance.setObjectName("appearance")
        self.verticalLayout_24.addWidget(self.appearance)
        self.passwords = QtWidgets.QPushButton(self.settings_3)
        self.passwords.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.passwords.setFont(font)
        self.passwords.setStyleSheet("QPushButton{\n"
                                     "color: white;\n"
                                     "background: transparent;\n"
                                     "padding-left: 10px;\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton::hover{\n"
                                     "    color: white;\n"
                                     "    background-color : rgba(255, 255  ,255 ,50);\n"
                                     "\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton::pressed{\n"
                                     "    background-color: rgba(255, 255, 255, 80)\n"
                                     "}\n"
                                     "")
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap("assets/resources/images/icons8-orthogonal-view-25.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)
        self.passwords.setIcon(icon19)
        self.passwords.setIconSize(QtCore.QSize(35, 35))
        self.passwords.setObjectName("passwords")
        self.verticalLayout_24.addWidget(self.passwords)
        self.startup = QtWidgets.QPushButton(self.settings_3)
        self.startup.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.startup.setFont(font)
        self.startup.setStyleSheet("QPushButton{\n"
                                   "color: white;\n"
                                   "background: transparent;\n"
                                   "padding-left: 10px;\n"
                                   "}\n"
                                   "\n"
                                   "QPushButton::hover{\n"
                                   "    color: white;\n"
                                   "    background-color : rgba(255, 255  ,255 ,50);\n"
                                   "\n"
                                   "}\n"
                                   "\n"
                                   "QPushButton::pressed{\n"
                                   "    background-color: rgba(255, 255, 255, 80)\n"
                                   "}\n"
                                   "")
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap(""
                                       "assets/resources/images/startup.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.startup.setIcon(icon20)
        self.startup.setIconSize(QtCore.QSize(35, 35))
        self.startup.setObjectName("startup")
        self.verticalLayout_24.addWidget(self.startup)
        self.controller = QtWidgets.QPushButton(self.settings_3)
        self.controller.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.controller.setFont(font)
        self.controller.setStyleSheet("QPushButton{\n"
                                      "color: white;\n"
                                      "background: transparent;\n"
                                      "padding-left: 10px;\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton::hover{\n"
                                      "    color: white;\n"
                                      "    background-color : rgba(255, 255  ,255 ,50);\n"
                                      "\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton::pressed{\n"
                                      "    background-color: rgba(255, 255, 255, 80)\n"
                                      "}\n"
                                      "")
        icon21 = QtGui.QIcon()
        icon21.addPixmap(QtGui.QPixmap("assets/resources/images/icons8-load-resume-template-25.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.controller.setIcon(icon21)
        self.controller.setIconSize(QtCore.QSize(35, 35))
        self.controller.setObjectName("controller")
        self.verticalLayout_24.addWidget(self.controller)
        self.hidden_files = QtWidgets.QPushButton(self.settings_3)
        self.hidden_files.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.hidden_files.setFont(font)
        self.hidden_files.setStyleSheet("QPushButton{\n"
                                        "color: white;\n"
                                        "background: transparent;\n"
                                        "padding-left: 10px;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton::hover{\n"
                                        "    color: white;\n"
                                        "    background-color : rgba(255, 255  ,255 ,50);\n"
                                        "\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton::pressed{\n"
                                        "    background-color: rgba(255, 255, 255, 80)\n"
                                        "}\n"
                                        "")
        icon22 = QtGui.QIcon()
        icon22.addPixmap(QtGui.QPixmap("assets/resources/images/icons8-show-non-hidden-views-35.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hidden_files.setIcon(icon22)
        self.hidden_files.setIconSize(QtCore.QSize(30, 30))
        self.hidden_files.setObjectName("hidden_files")
        self.verticalLayout_24.addWidget(self.hidden_files)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_24.addItem(spacerItem9)
        self.line_4 = QtWidgets.QFrame(self.settings_3)
        self.line_4.setMaximumSize(QtCore.QSize(16777215, 1))
        self.line_4.setStyleSheet("background-color: rgba(255, 255, 255, 80);\n"
                                  "color: rgba(255, 255, 255, 80);\n"
                                  "margin-left: 15px;\n"
                                  "margin-right: 25px;")
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_24.addWidget(self.line_4)
        self.feedback = QtWidgets.QPushButton(self.settings_3)
        self.feedback.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.feedback.setFont(font)
        self.feedback.setStyleSheet("QPushButton{\n"
                                    "color: white;\n"
                                    "background: transparent;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton::hover{\n"
                                    "    color: white;\n"
                                    "    background-color : rgba(255, 255  ,255 ,50);\n"
                                    "\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton::pressed{\n"
                                    "    background-color: rgba(255, 255, 255, 80)\n"
                                    "}\n"
                                    "")
        icon23 = QtGui.QIcon()
        icon23.addPixmap(QtGui.QPixmap("assets/resources/images/feedback.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.feedback.setIcon(icon23)
        self.feedback.setIconSize(QtCore.QSize(30, 30))
        self.feedback.setObjectName("feedback")
        self.verticalLayout_24.addWidget(self.feedback, 0, QtCore.Qt.AlignBottom)
        self.verticalLayout_23.addLayout(self.verticalLayout_24)
        self.horizontalLayout_3.addWidget(self.settings_3)
        self.gridLayout_8.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.stackedWidget = QtWidgets.QStackedWidget(self.settings1)
        self.stackedWidget.setObjectName("stackedWidget")
        self.appearance_2 = QtWidgets.QWidget()
        self.appearance_2.setObjectName("appearance_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.appearance_2)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.appearance_frame = QtWidgets.QFrame(self.appearance_2)
        self.appearance_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.appearance_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.appearance_frame.setObjectName("appearance_frame")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.appearance_frame)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.appearance_label = QtWidgets.QPushButton(self.appearance_frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.appearance_label.setFont(font)
        self.appearance_label.setStyleSheet("color: white; background: transparent;")
        icon24 = QtGui.QIcon()
        icon24.addPixmap(
            QtGui.QPixmap("assets/resources/images/appearance.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.appearance_label.setIcon(icon24)
        self.appearance_label.setIconSize(QtCore.QSize(35, 35))
        self.appearance_label.setObjectName("appearance_label")
        self.verticalLayout_9.addWidget(self.appearance_label, 0, QtCore.Qt.AlignTop)
        self.effect_label = QtWidgets.QLabel(self.appearance_frame)
        font = QtGui.QFont()
        font.setFamily("Segoe MVR MDL2 Animation")
        font.setPointSize(14)
        self.effect_label.setFont(font)
        self.effect_label.setStyleSheet("color: white;\n"
                                        "margin-top: 10px;")
        self.effect_label.setObjectName("effect_label")
        self.verticalLayout_9.addWidget(self.effect_label)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setContentsMargins(40, -1, -1, -1)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        spacerItem10 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_11.addItem(spacerItem10)
        self.effect_radiobutton = QtWidgets.QRadioButton(self.appearance_frame)
        self.effect_radiobutton.setMinimumSize(QtCore.QSize(0, 35))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setItalic(False)
        self.effect_radiobutton.setFont(font)
        self.effect_radiobutton.setStyleSheet("QRadioButton{\n"
                                              "    color: white;\n"
                                              "}\n"
                                              "\n"
                                              "QRadioButton::indicator {\n"
                                              "    border: 3px solid rgb(52, 59, 72);\n"
                                              "    width: 15px;\n"
                                              "    color: white; \n"
                                              "    text-align: center;\n"
                                              "    height: 15px;\n"
                                              "    border-radius: 10px;\n"
                                              "    background: rgb(44, 49, 60);\n"
                                              "}\n"
                                              "QRadioButton::indicator:hover {\n"
                                              "     border: 3px solid rgb(58, 66, 81);\n"
                                              "}\n"
                                              "QRadioButton::indicator:checked {\n"
                                              "    background: 3px solid rgb(94, 106, 130);\n"
                                              "    border: 3px solid rgb(52, 59, 72);\n"
                                              "}")
        self.effect_radiobutton.setObjectName("effect_radiobutton")
        self.verticalLayout_11.addWidget(self.effect_radiobutton)
        self.theme_box = QtWidgets.QComboBox(self.appearance_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.theme_box.sizePolicy().hasHeightForWidth())
        self.theme_box.setSizePolicy(sizePolicy)
        self.theme_box.setMinimumSize(QtCore.QSize(200, 35))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.theme_box.setFont(font)
        self.theme_box.setStyleSheet("QComboBox{\n"
                                     "   background-color: rgba(27, 29, 35, 40);\n"
                                     "   border-radius: 5px;\n"
                                     "  border: 2px solid rgb(33, 37, 43);\n"
                                     "  padding: 5px;\n"
                                     "color: white;\n"
                                     " padding-left: 10px;\n"
                                     "}\n"
                                     "QComboBox:hover{\n"
                                     "   border: 2px solid rgb(64, 71, 88);\n"
                                     "}\n"
                                     "QComboBox::drop-down {\n"
                                     "   subcontrol-origin: padding;\n"
                                     "  subcontrol-position: top right;\n"
                                     "  width: 25px; \n"
                                     "  border-left-width: 3px;\n"
                                     " border-left-color: rgba(39, 44, 54, 150);\n"
                                     "    border-left-style: solid;\n"
                                     "  border-top-right-radius: 3px;\n"
                                     "  border-bottom-right-radius: 3px;\n"
                                     "  background-image: url(assets/resources/images/arror.png);\n"
                                     " background-position: center;\n"
                                     " background-repeat: no-reperat;\n"
                                     "}\n"
                                     "QComboBox QAbstractItemView {\n"
                                     "  color: rgb(255, 121, 198);\n"
                                     "   background-color: rgb(33, 37, 43);\n"
                                     "   padding: 10px;\n"
                                     "   selection-background-color: rgb(39, 44, 54);\n"
                                     "}")
        self.theme_box.setObjectName("theme_box")
        self.theme_box.addItem("")
        self.theme_box.addItem("")
        self.theme_box.addItem("")
        self.theme_box.addItem("")
        self.theme_box.addItem("")
        self.theme_box.addItem("")
        self.theme_box.addItem("")
        self.verticalLayout_11.addWidget(self.theme_box)
        spacerItem11 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_11.addItem(spacerItem11)
        self.additional_settings_layout = QtWidgets.QGridLayout()
        self.additional_settings_layout.setHorizontalSpacing(5)
        self.additional_settings_layout.setVerticalSpacing(10)
        self.additional_settings_layout.setObjectName("additional_settings_layout")
        self.tint = QtWidgets.QPushButton(self.appearance_frame)
        self.tint.setMinimumSize(QtCore.QSize(10, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.tint.setFont(font)
        self.tint.setStyleSheet("text-align: left;\n"
                                "background: transparent;\n"
                                "color: white;\n"
                                "margin-left: 35px;")
        self.tint.setObjectName("tint")
        self.additional_settings_layout.addWidget(self.tint, 1, 0, 1, 1)
        self.tint_slider = QtWidgets.QSlider(self.appearance_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tint_slider.sizePolicy().hasHeightForWidth())
        self.tint_slider.setSizePolicy(sizePolicy)
        self.tint_slider.setMinimumSize(QtCore.QSize(120, 0))
        self.tint_slider.setStyleSheet("QSlider::groove:horizontal {\n"
                                       "    border:1px solid rgba(255, 255, 255, 0.30);\n"
                                       "    height: 8px;\n"
                                       "    background: :rgba(255, 255, 255, 0.30); \n"
                                       "    margin: 2px 0;\n"
                                       "}\n"
                                       "\n"
                                       "QSlider::handle:horizontal {\n"
                                       "    background: rgba(255, 255, 255, 0.30);\n"
                                       "    border: 1px ;\n"
                                       "    width: 5px;\n"
                                       "    margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */\n"
                                       "    border-radius: 10px;\n"
                                       "}\n"
                                       "\n"
                                       "QSlider::sub-page:horizontal {\n"
                                       "                border-radius :3px;\n"
                                       "                background-color: rgba(255, 255, 255, 0.30);\n"
                                       "                }")
        self.tint_slider.setMaximum(100)
        self.tint_slider.setProperty("value", 0)
        self.tint_slider.setOrientation(QtCore.Qt.Horizontal)
        self.tint_slider.setObjectName("tint_slider")
        self.additional_settings_layout.addWidget(self.tint_slider, 1, 1, 1, 1)
        self.radius = QtWidgets.QPushButton(self.appearance_frame)
        self.radius.setMinimumSize(QtCore.QSize(100, 0))
        self.radius.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.radius.setFont(font)
        self.radius.setStyleSheet("text-align: left;\n"
                                  "background: transparent;\n"
                                  "color: white;\n"
                                  "margin-left: 35px;")
        self.radius.setObjectName("radius")
        self.additional_settings_layout.addWidget(self.radius, 2, 0, 1, 1)
        self.radius_slider = QtWidgets.QSlider(self.appearance_frame)
        self.radius_slider.setMinimumSize(QtCore.QSize(120, 0))
        self.radius_slider.setStyleSheet("QSlider::groove:horizontal {\n"
                                         "    border:1px solid rgba(255, 255, 255, 0.30);\n"
                                         "    height: 8px;\n"
                                         "    background: :rgba(255, 255, 255, 0.30); \n"
                                         "    margin: 2px 0;\n"
                                         "}\n"
                                         "\n"
                                         "QSlider::handle:horizontal {\n"
                                         "    background: rgba(255, 255, 255, 0.30);\n"
                                         "    border: 1px ;\n"
                                         "    width: 5px;\n"
                                         "    margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */\n"
                                         "    border-radius: 10px;\n"
                                         "}\n"
                                         "\n"
                                         "QSlider::sub-page:horizontal {\n"
                                         "                border-radius :3px;\n"
                                         "                background-color: rgba(255, 255, 255, 0.30);\n"
                                         "                }")
        self.radius_slider.setMaximum(100)
        self.radius_slider.setOrientation(QtCore.Qt.Horizontal)
        self.radius_slider.setObjectName("radius_slider")
        self.additional_settings_layout.addWidget(self.radius_slider, 2, 1, 1, 1, QtCore.Qt.AlignHCenter)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.additional_settings_layout.addItem(spacerItem12, 1, 3, 1, 1)
        self.additional_settings = QtWidgets.QPushButton(self.appearance_frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.additional_settings.setFont(font)
        self.additional_settings.setStyleSheet("text-align: left;\n"
                                               "background: transparent;\n"
                                               "color: white;")
        self.additional_settings.setObjectName("additional_settings")
        self.additional_settings_layout.addWidget(self.additional_settings, 0, 0, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.additional_settings_layout.addItem(spacerItem13, 1, 2, 1, 1)
        self.verticalLayout_11.addLayout(self.additional_settings_layout)
        spacerItem14 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_11.addItem(spacerItem14)
        self.verticalLayout_9.addLayout(self.verticalLayout_11)
        self.horizontalLayout_6.addWidget(self.appearance_frame)
        self.verticalScrollBar = QtWidgets.QScrollBar(self.appearance_2)
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.horizontalLayout_6.addWidget(self.verticalScrollBar)
        self.stackedWidget.addWidget(self.appearance_2)
        self.startup_page = QtWidgets.QWidget()
        self.startup_page.setObjectName("startup_page")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.startup_page)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.startup_frame = QtWidgets.QFrame(self.startup_page)
        self.startup_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.startup_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.startup_frame.setObjectName("startup_frame")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.startup_frame)
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setContentsMargins(20, -1, -1, -1)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        spacerItem15 = QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_12.addItem(spacerItem15)
        self.start_up_label = QtWidgets.QPushButton(self.startup_frame)
        self.start_up_label.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.start_up_label.setFont(font)
        self.start_up_label.setStyleSheet("color: white; background: transparent;")
        icon25 = QtGui.QIcon()
        icon25.addPixmap(
            QtGui.QPixmap("assets/resources/images/startup.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.start_up_label.setIcon(icon25)
        self.start_up_label.setIconSize(QtCore.QSize(35, 35))
        self.start_up_label.setObjectName("start_up_label")
        self.verticalLayout_12.addWidget(self.start_up_label, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        spacerItem16 = QtWidgets.QSpacerItem(20, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_12.addItem(spacerItem16)
        self.new_tab_toggle = QtWidgets.QRadioButton(self.startup_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.new_tab_toggle.sizePolicy().hasHeightForWidth())
        self.new_tab_toggle.setSizePolicy(sizePolicy)
        self.new_tab_toggle.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe MVR MDL2 Animation")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.new_tab_toggle.setFont(font)
        self.new_tab_toggle.setStyleSheet("QRadioButton{\n"
                                          "    color: white;\n"
                                          "}\n"
                                          "\n"
                                          "QRadioButton::indicator {\n"
                                          "    border: 3px solid rgb(52, 59, 72);\n"
                                          "    width: 15px;\n"
                                          "    color: white; \n"
                                          "    text-align: center;\n"
                                          "    height: 15px;\n"
                                          "    border-radius: 10px;\n"
                                          "    background: rgb(44, 49, 60);\n"
                                          "}\n"
                                          "QRadioButton::indicator:hover {\n"
                                          "     border: 3px solid rgb(58, 66, 81);\n"
                                          "}\n"
                                          "QRadioButton::indicator:checked {\n"
                                          "    background: 3px solid rgb(94, 106, 130);\n"
                                          "    border: 3px solid rgb(52, 59, 72);\n"
                                          "}")
        self.new_tab_toggle.setObjectName("new_tab_toggle")
        self.verticalLayout_12.addWidget(self.new_tab_toggle)
        self.left_off = QtWidgets.QRadioButton(self.startup_frame)
        self.left_off.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe MVR MDL2 Animation")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.left_off.setFont(font)
        self.left_off.setStyleSheet("QRadioButton{\n"
                                    "    color: white;\n"
                                    "}\n"
                                    "\n"
                                    "QRadioButton::indicator {\n"
                                    "    border: 3px solid rgb(52, 59, 72);\n"
                                    "    width: 15px;\n"
                                    "    color: white; \n"
                                    "    text-align: center;\n"
                                    "    height: 15px;\n"
                                    "    border-radius: 10px;\n"
                                    "    background: rgb(44, 49, 60);\n"
                                    "}\n"
                                    "QRadioButton::indicator:hover {\n"
                                    "     border: 3px solid rgb(58, 66, 81);\n"
                                    "}\n"
                                    "QRadioButton::indicator:checked {\n"
                                    "    background: 3px solid rgb(94, 106, 130);\n"
                                    "    border: 3px solid rgb(52, 59, 72);\n"
                                    "}")
        self.left_off.setObjectName("left_off")
        self.verticalLayout_12.addWidget(self.left_off)
        self.specific_page = QtWidgets.QRadioButton(self.startup_frame)
        self.specific_page.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe MVR MDL2 Animation")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.specific_page.setFont(font)
        self.specific_page.setStyleSheet("QRadioButton{\n"
                                         "    color: white;\n"
                                         "}\n"
                                         "\n"
                                         "QRadioButton::indicator {\n"
                                         "    border: 3px solid rgb(52, 59, 72);\n"
                                         "    width: 15px;\n"
                                         "    color: white; \n"
                                         "    text-align: center;\n"
                                         "    height: 15px;\n"
                                         "    border-radius: 10px;\n"
                                         "    background: rgb(44, 49, 60);\n"
                                         "}\n"
                                         "QRadioButton::indicator:hover {\n"
                                         "     border: 3px solid rgb(58, 66, 81);\n"
                                         "}\n"
                                         "QRadioButton::indicator:checked {\n"
                                         "    background: 3px solid rgb(94, 106, 130);\n"
                                         "    border: 3px solid rgb(52, 59, 72);\n"
                                         "}")
        self.specific_page.setObjectName("specific_page")
        self.verticalLayout_12.addWidget(self.specific_page)
        spacerItem17 = QtWidgets.QSpacerItem(20, 7, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_12.addItem(spacerItem17)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem18, 0, 2, 1, 1)
        self.specific_page_url = QtWidgets.QLineEdit(self.startup_frame)
        self.specific_page_url.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.specific_page_url.sizePolicy().hasHeightForWidth())
        self.specific_page_url.setSizePolicy(sizePolicy)
        self.specific_page_url.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.specific_page_url.setFont(font)
        self.specific_page_url.setStyleSheet("QLineEdit {\n"
                                             "    color: white;\n"
                                             "   border-radius: 5px;\n"
                                             "   border: 2px solid rgb(33, 37, 43);\n"
                                             "   padding-left: 10px;\n"
                                             "   selection-color: rgb(255, 255, 255);\n"
                                             "   selection-background-color: rgb(255, 121, 198);\n"
                                             "}\n"
                                             "\n"
                                             "QLineEdit:hover {\n"
                                             "   border: 2px solid rgb(64, 71, 88);\n"
                                             "    background-color: rgba(255, 255, 255, 30)\n"
                                             "}\n"
                                             "\n"
                                             "QLineEdit:focus {\n"
                                             "  border: 2px solid rgb(91, 101, 124);\n"
                                             "}")
        self.specific_page_url.setText("")
        self.specific_page_url.setObjectName("specific_page_url")
        self.gridLayout_3.addWidget(self.specific_page_url, 0, 1, 1, 1)
        spacerItem19 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem19, 1, 1, 1, 1)
        spacerItem20 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem20, 0, 0, 1, 1)
        self.verticalLayout_12.addLayout(self.gridLayout_3)
        self.verticalLayout_13.addLayout(self.verticalLayout_12)
        self.verticalLayout_14.addWidget(self.startup_frame)
        self.stackedWidget.addWidget(self.startup_page)
        self.feedback_page = QtWidgets.QWidget()
        self.feedback_page.setObjectName("feedback_page")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.feedback_page)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_11 = QtWidgets.QGridLayout()
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.feedback_frame = QtWidgets.QFrame(self.feedback_page)
        self.feedback_frame.setStyleSheet("background-color: rgba(0,0,0,0.0)")
        self.feedback_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.feedback_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.feedback_frame.setObjectName("feedback_frame")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.feedback_frame)
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout()
        self.verticalLayout_19.setContentsMargins(20, -1, 20, -1)
        self.verticalLayout_19.setSpacing(0)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.label_3 = QtWidgets.QLabel(self.feedback_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: white; background: transparent;")
        self.label_3.setText("")
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_19.addWidget(self.label_3)
        self.feedback_graphics_frame = QtWidgets.QFrame(self.feedback_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.feedback_graphics_frame.sizePolicy().hasHeightForWidth())
        self.feedback_graphics_frame.setSizePolicy(sizePolicy)
        self.feedback_graphics_frame.setMinimumSize(QtCore.QSize(0, 200))
        self.feedback_graphics_frame.setStyleSheet("background: transparent;")
        self.feedback_graphics_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.feedback_graphics_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.feedback_graphics_frame.setObjectName("feedback_graphics_frame")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout(self.feedback_graphics_frame)
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.verticalLayout_22 = QtWidgets.QVBoxLayout()
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.label_2 = QtWidgets.QLabel(self.feedback_graphics_frame)
        self.label_2.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: white; background: transparent;")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_22.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        spacerItem21 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_22.addItem(spacerItem21)
        self.label_4 = QtWidgets.QLabel(self.feedback_graphics_frame)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: white; background: transparent;")
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_22.addWidget(self.label_4)
        spacerItem22 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_22.addItem(spacerItem22)
        self.verticalLayout_21.addLayout(self.verticalLayout_22)
        self.verticalLayout_19.addWidget(self.feedback_graphics_frame)
        self.gridLayout_15 = QtWidgets.QGridLayout()
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.sent_ui = QtWidgets.QPushButton(self.feedback_frame)
        self.sent_ui.setMinimumSize(QtCore.QSize(0, 200))
        self.sent_ui.setMaximumSize(QtCore.QSize(210, 16777215))
        self.sent_ui.setStyleSheet("QPushButton{\n"
                                   "    background: transparent;\n"
                                   "    color: white;\n"
                                   "    border-radius: 100px;\n"
                                   "    background-color : rgba(255, 255  ,255 ,50);\n"
                                   "}")
        self.sent_ui.setText("")
        icon26 = QtGui.QIcon()
        icon26.addPixmap(
            QtGui.QPixmap("assets/resources/images/mark96.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sent_ui.setIcon(icon26)
        self.sent_ui.setIconSize(QtCore.QSize(96, 96))
        self.sent_ui.setObjectName("sent_ui")
        self.gridLayout_15.addWidget(self.sent_ui, 0, 0, 1, 1)
        self.response = QtWidgets.QPushButton(self.feedback_frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.response.setFont(font)
        self.response.setStyleSheet("color: white; background: transparent;")
        self.response.setObjectName("response")
        self.gridLayout_15.addWidget(self.response, 2, 0, 1, 1)
        spacerItem23 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_15.addItem(spacerItem23, 1, 0, 1, 1)
        self.verticalLayout_19.addLayout(self.gridLayout_15)
        self.write_to_us_box = QtWidgets.QPlainTextEdit(self.feedback_frame)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.write_to_us_box.setFont(font)
        self.write_to_us_box.setStyleSheet("color: white;\n"
                                           " background: transparent; \n"
                                           "border: 0;\n"
                                           "margin-left: 10px;r")
        self.write_to_us_box.setBackgroundVisible(True)
        self.write_to_us_box.setObjectName("write_to_us_box")
        self.verticalLayout_19.addWidget(self.write_to_us_box)
        spacerItem24 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_19.addItem(spacerItem24)
        self.send_feedback = QtWidgets.QPushButton(self.feedback_frame)
        self.send_feedback.setMinimumSize(QtCore.QSize(0, 45))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.send_feedback.setFont(font)
        self.send_feedback.setStyleSheet("QPushButton{\n"
                                         "color: white;\n"
                                         "background: transparent;\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton::hover{\n"
                                         "    color: white;\n"
                                         "    background-color : rgba(255, 255  ,255 ,50);\n"
                                         "\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton::pressed{\n"
                                         "    background-color: rgba(255, 255, 255, 80)\n"
                                         "}\n"
                                         "")
        self.send_feedback.setObjectName("send_feedback")
        self.verticalLayout_19.addWidget(self.send_feedback)
        self.write_to_us = QtWidgets.QPushButton(self.feedback_frame)
        self.write_to_us.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.write_to_us.setFont(font)
        self.write_to_us.setStyleSheet("QPushButton{\n"
                                       "color: white;\n"
                                       "background: transparent;\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton::hover{\n"
                                       "    color: white;\n"
                                       "    background-color : rgba(255, 255  ,255 ,50);\n"
                                       "\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton::pressed{\n"
                                       "    background-color: rgba(255, 255, 255, 80)\n"
                                       "}\n"
                                       "")
        icon27 = QtGui.QIcon()
        icon27.addPixmap(QtGui.QPixmap(
            "assets/resources/images/icons8-contact-us-48.png"),
                         QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.write_to_us.setIcon(icon27)
        self.write_to_us.setIconSize(QtCore.QSize(35, 35))
        self.write_to_us.setObjectName("write_to_us")
        self.verticalLayout_19.addWidget(self.write_to_us)
        spacerItem25 = QtWidgets.QSpacerItem(20, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_19.addItem(spacerItem25)
        self.verticalLayout_17.addLayout(self.verticalLayout_19)
        self.gridLayout_11.addWidget(self.feedback_frame, 0, 0, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_11)
        self.stackedWidget.addWidget(self.feedback_page)
        self.gridLayout_8.addWidget(self.stackedWidget, 0, 2, 1, 1)
        self.line = QtWidgets.QFrame(self.settings1)
        self.line.setMaximumSize(QtCore.QSize(1, 16777215))
        self.line.setStyleSheet("background-color:  rgba(255, 255, 255, 30);\n"
                                "color: rgba(255, 255, 255, 30);\n"
                                "margin-left: 15px;\n"
                                "margin-right: 15px;")
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_8.addWidget(self.line, 0, 1, 1, 1)
        self.tabWidget.addTab(self.settings1, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.verticalLayout_6.addWidget(self.main_frame)
        self.main_stacked_widget.addWidget(self.main_pages)
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.page)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_7.addLayout(self.gridLayout_6, 0, 0, 1, 1)
        self.main_stacked_widget.addWidget(self.page)
        self.verticalLayout.addWidget(self.main_stacked_widget)
        self.main_layout.addWidget(self.window_frame)
        self.gridLayout.addWidget(self.all_frame, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.GDrive, self.thisPC)
        Form.setTabOrder(self.thisPC, self.downloads)
        Form.setTabOrder(self.downloads, self.videos)
        Form.setTabOrder(self.videos, self.settings)
        Form.setTabOrder(self.settings, self.minimize)
        Form.setTabOrder(self.minimize, self.maximize)
        Form.setTabOrder(self.maximize, self.close)
        Form.setTabOrder(self.close, self.pictures)
        Form.setTabOrder(self.pictures, self.collapse)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Fluent Explorer.exe"))
        self.collapse.setText(_translate("Form", "  Fluent Explorer"))
        self.search_box.setPlaceholderText(_translate("Form", "Search Anything"))
        self.GDrive.setText(_translate("Form", "   GDrive"))
        self.thisPC.setText(_translate("Form", "   This pc"))
        self.downloads.setText(_translate("Form", "   Downloads"))
        self.pictures.setText(_translate("Form", "   Pictures"))
        self.videos.setText(_translate("Form", "   Videos"))
        self.music.setText(_translate("Form", "   Music"))
        self.documents.setText(_translate("Form", "   Documents"))
        self.settings.setText(_translate("Form", "   Settings"))
        self.path.setPlaceholderText(_translate("Form", " Path :  "))
        self.this_pc_label.setText(_translate("Form", "This pc"))
        self.pushButton_6.setText(_translate("Form", "Drives"))
        self.pushButton_5.setText(_translate("Form", "Library"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.this_pc_2), _translate("Form", "  This pc           "))
        self.downloads_label.setText(_translate("Form", "Downloads"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.downloads_tab),
                                  _translate("Form", "  Downloads           "))
        self.this_pc_label_2.setText(_translate("Form", "Music"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.music_tab), _translate("Form", "  Music           "))
        self.settings_button.setText(_translate("Form", "  Settings "))
        self.settings_button.setShortcut(_translate("Form", "Ctrl+R"))
        self.appearance.setText(_translate("Form", "Appearance   "))
        self.passwords.setText(_translate("Form", " View Style     "))
        self.startup.setText(_translate("Form", "On Startup      "))
        self.controller.setText(_translate("Form", " Controller      "))
        self.hidden_files.setText(_translate("Form", " Hidden Files  "))
        self.feedback.setText(_translate("Form", "  Feedback  "))
        self.appearance_label.setText(_translate("Form", " Appearance"))
        self.effect_label.setText(_translate("Form", "Effects"))
        self.effect_radiobutton.setText(_translate("Form", "Elegant Effect"))
        self.theme_box.setItemText(0, _translate("Form", "Default"))
        self.theme_box.setItemText(1, _translate("Form", "Acrylic"))
        self.theme_box.setItemText(2, _translate("Form", "Transparent"))
        self.theme_box.setItemText(3, _translate("Form", "Blur"))
        self.theme_box.setItemText(4, _translate("Form", "Light"))
        self.theme_box.setItemText(5, _translate("Form", "Dark"))
        self.theme_box.setItemText(6, _translate("Form", "Amoled"))
        self.tint.setText(_translate("Form", "Tint"))
        self.radius.setText(_translate("Form", "Radius"))
        self.additional_settings.setText(_translate("Form", "Additional Settings "))
        self.start_up_label.setText(_translate("Form", " StartUp"))
        self.new_tab_toggle.setText(_translate("Form", "Open a net tab."))
        self.left_off.setText(_translate("Form", "Continue where you left."))
        self.specific_page.setText(_translate("Form", "Open a specific page."))
        self.specific_page_url.setPlaceholderText(_translate("Form", "Address"))
        self.label_2.setText(_translate("Form", "Help & Feedback"))
        self.label_4.setText(_translate("Form",
                                        "You can make contribution in the development of this software  by telling us what you do not like about this application at Legendawaken4@gmail.com. This app is under development please contact us and report your issue it may get fixed in the next release."))
        self.response.setText(_translate("Form", "Thank You for your feedback."))
        self.send_feedback.setText(_translate("Form", "Send Feedback."))
        self.write_to_us.setText(_translate("Form", "  Write to Us "))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings1), _translate("Form", "  Settings           "))

    def additional_settings_manager(self, *args):
        for i in args:
            if i == 'set_default':
                with open('rep32.dll', 'r') as theme_reader:
                    read_theme = theme_reader.read()
                if read_theme == 'transparent':
                    self.additional_settings_manager('tint_only')
                elif read_theme == 'blur':
                    self.additional_settings_manager('set_visible')
                else:
                    self.additional_settings_manager('set_invisible')

            if i == 'set_visible':
                self.additional_settings.setVisible(True)
                self.tint.setVisible(True)
                self.radius.setVisible(True)
                self.tint_slider.setVisible(True)
                self.radius_slider.setVisible(True)
            if i == 'set_invisible':
                self.additional_settings.setVisible(False)
                self.tint.setVisible(False)
                self.radius.setVisible(False)
                self.tint_slider.setVisible(False)
                self.radius_slider.setVisible(False)
            if i == 'tint_only':
                self.additional_settings.setVisible(True)
                self.tint.setVisible(True)
                self.tint_slider.setVisible(True)
                self.radius.setVisible(False)
                self.radius_slider.setVisible(False)
            if i == 'radius_only':
                self.additional_settings.setVisible(True)
                self.tint.setVisible(False)
                self.tint_slider.setVisible(False)
                self.radius.setVisible(True)
                self.radius_slider.setVisible(True)


    def set_acrylic(self, val=True or False, *args):
        if val:
            for i in args:
                if i == "set_all":
                    if self.isMaximized():
                        self.all_frame.setStyleSheet(f"""background: transparent;""")
                        self.window_frame.setStyleSheet(f"""background: transparent;""")
                        self.graphics.setStyleSheet(f"""background: transparent;""")

                        with open("assets/resources/holder.tru", "r") as reader:
                            r = str(reader.read())

                        self.all_frame.setStyleSheet(f"""
                            background: transparent;
                            background: url('C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_reb1{r}.jpeg');
                            background-repeat: no-repeat;
                            background-position: left;
                            border: 0;""")

                if i == "set_on_left" or i == 'default':

                    with open("assets/resources/holder.tru", "r") as reader:
                        r = str(reader.read())
                    self.all_frame.setStyleSheet(f"""
                        background:  url('C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_reb1{r}.jpeg');
                        background-repeat: no-repeat;
                        background-position: left;
                        border: 0;""")
                    self.window_frame.setStyleSheet("background: black;")

                if i == "set_on_right":
                    with open("assets/resources/holder.tru", "r") as reader:
                        r = str(reader.read())
                    self.window_frame.setStyleSheet(f"""
                        background: transparent;
                        background: url('C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_reb1{r}.jpeg');
                        background-repeat: no-repeat;
                        background-position: right;
                        border: 0;""")

            return
        else:
            for i in args:
                if i == "amoled":
                    self.all_frame.setStyleSheet("""background: black;""")
                    self.window_frame.setStyleSheet("""background: black;""")
                    self.graphics.setStyleSheet("""background: black;""")
                if i == "dark":
                    self.all_frame.setStyleSheet(f"""background: rgb(40, 40, 40);""")
                    self.window_frame.setStyleSheet(f"""background: rgb(40, 40, 40);""")
                    self.graphics.setStyleSheet(f"""background: rgb(30, 30, 30);""")
                    # ThemeHandler(MainWindow=self)
                if i == "light":
                    # self.all_frame.setStyleSheet(f"""
                    # background-color: rgb(255, 255, 255);
                    # foreground-color: rgb(0, 0, 0);
                    # color: rgb(0, 0, 0)""")
                    # self.window_frame.setStyleSheet(f"""
                    # background-color: rgb(255, 255, 255)""")
                    # ThemeHandler(MainWindow=self)
                    ToastNotifier().show_toast(msg='Theme is not available at the moment. This might be fixed in future '
                                                   'update.',
                                               title='Theme Unavailable.', threaded= True)
                if i == "transparent":
                    self.all_frame.setStyleSheet(f"""background: 	transparent;""")
                    self.window_frame.setStyleSheet(f"""background: transparent;""")
                    self.graphics.setStyleSheet(f"""background: transparent;""")
                if i == 'semi-transparent':
                    self.all_frame.setStyleSheet(f"""background: rgba(0, 0, 0, 170);""")
                    self.window_frame.setStyleSheet(f"""background: rgba(0, 0, 0, 170);""")
                    self.graphics.setStyleSheet(f"""background: rgba(0, 0, 0, 170);""")
                    # self.setWindowOpacity(1.0)

    def setup_elegantUi(self):
        if self.isMaximized():
            if self.effect_radiobutton.isChecked():
                # self.set_acrylic(True, "set_all")
                self.setTheme()
                with open("lib.dll", "w") as writer:
                    writer.write("True")
            else:
                # # self.set_acrylic(False, 'dark')
                # self.setTheme()
                with open('rep32.dll', 'r') as reader:
                    read = reader.read()
                if read == 'blur' or read == 'acrylic':
                    self.set_acrylic(True,'set_on_left')
                    self.window_frame.setStyleSheet("background: black;")
                elif read == 'dark':
                    self.setTheme(theme='dark')
                elif read == 'amoled':
                    self.setTheme('amoled')
                else:
                    self.setTheme('semi-transparent')
                with open("lib.dll", "w") as writer:
                    writer.write("False")

    def slideMenu(self, value= True or False):
        width = self.graphics.width()

        if value:
            # decrease the slide menu size

            # set name
            self.collapse.setText("")
            self.search_box.setVisible(False)
            # self.search.setMaximumWidth(20)
            self.search.setStyleSheet("""
                QPushButton{
color: white;
background: transparent;
padding-right: 5px;
	
}

QPushButton::hover{
	color: white;
	background-color : rgba(255, 255  ,255 ,50);

}

QPushButton::pressed{
	background-color: rgba(255, 255, 255, 80)
}
            """)

            #
            # if width == 380:
            #     new_width = 45
            # else:
            #     new_width = 380
            #
            #
            # self.animation = QtCore.QPropertyAnimation(self.graphics, b"maximumWidth", self)
            # self.animation.setStartValue(width)
            # self.animation.setEndValue(new_width)
            # self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            # self.animation.setDuration(200)
            # self.animation.start()

            self.graphics.setMaximumWidth(10)
            self.graphics.setMinimumWidth(45)

            self.gdrive_line.setVisible(False)
            self.settings_line.setVisible(False)



            return -1

        else:
            # increae the size
            # set name
            self.collapse.setText("  Fluent Explorer")
            self.search.setStyleSheet("""
                QPushButton{
                    color: white;
                    background: transparent;
                    padding-right: 5px;
                    }
 """)

            # if width == 45:
            #     new_width = 380
            # else:
            #     new_width = 45
            #
            #
            # self.animation_down = QtCore.QPropertyAnimation(self.graphics, b"minimumWidth", self)
            # self.animation_down.setStartValue(45)
            # self.animation_down.setEndValue(350)
            # self.animation_down.setEasingCurve(QtCore.QEasingCurve.InElastic)
            # self.animation_down.setDuration(200)
            # self.animation_down.start()
            #
            # print("Down Width : ", width)

            # self.search.setMaximumWidth(200)
            self.graphics.setMaximumWidth(380)
            self.graphics.setMinimumWidth(350)

            self.search_box.setVisible(True)
            self.gdrive_line.setVisible(True)
            self.settings_line.setVisible(True)
            # self.search_clear.setVisible(True)

    def menu_handler(self):

        with open("assets/resources/Core.dll", "r") as reader:
            read = reader.read()

        if read == "True":
            self.slideMenu(False)
            with open("assets/resources/Core.dll", "w") as writer:
                writer.write("False")

            self.search.clicked.connect(lambda: self.slideMenu(False))

        else:
            self.slideMenu(True)
            with open("assets/resources/Core.dll", "w") as writer:
                writer.write("True")

    def fluentHandler(self):
        # FRAME 1
        with open("assets/resources/holder.tru", "r") as reader_:
            r = str(reader_.read())

        self.graphics.setStyleSheet(f"""
                                   background: url(C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_reb1{r}.jpeg);
                                   background-repeat: repeat;
                                   background-position: left;
                                   border: 0;""")

    def min(self):
        self.showMinimized()

    def max_reduce(self):
        if self.isMaximized():
            self.showNormal()
            icon = QIcon()
            icon.addFile("assets/resources/images/maximize.png", QSize(), QIcon.Normal, QIcon.Off)
            self.slideMenu(value=True)
            self.maximize.setIcon(icon)
            self.set_acrylic(False, 'dark')
            self.additional_settings_manager('set_invisible')
        else:
            self.showMaximized()
            icon = QIcon()
            icon.addFile("assets/resources/images/estore.png", QSize(), QIcon.Normal, QIcon.Off)
            self.maximize.setIcon(icon)
            self.set_acrylic(True)
            self.additional_settings_manager('set_default')

    def stop(self):
        app.closeAllWindows()
        sys.exit()

    def temp_checksum(self):
        if not os.path.isfile(f'C:/Users/{GetUserName()}/AppData/Local/Temp/CachedData/mr.tru'):
            try:
                os.makedirs(f'C:/Users/{GetUserName()}/AppData/Local/Temp/CachedData/cache')
                self.music_indexer()
            except FileExistsError:
                pass
# ################################################### Main UI ######################################################
    # ************************* This Pc *************************** #
    def thisPC_UI(self):
        # drives = GetLogicalDriveStrings()
        # lst = []
        # for i in drives:
        #     if str(i).isalpha():
        #         lst.append("  " + i)
        library_lst = ['  Downloads', '  Music', '  Pictures', '  Videos', '  Documents']
        for i in range(5):
            pushbuton = QPushButton(f"{library_lst[i]}")
            pushbuton.setMinimumSize(150, 90)
            # pushbuton.setMaximumSize(200, 150)

            pushbuton.setFont(QFont("Segoe UI", 14))

            if library_lst[i] == "  Downloads":
                pushbuton.setIcon(QIcon("assets/resources/images/downloads.png"))
                pushbuton.setIconSize(QSize(25, 25))
            if library_lst[i] == "  Music":
                pushbuton.setIcon(QIcon("assets/resources/images/music25.png"))
                pushbuton.setIconSize(QSize(45, 45))
            if library_lst[i] == "  Pictures":
                pushbuton.setIcon(QIcon("assets/resources/images/picture25.png"))
                pushbuton.setIconSize(QSize(30, 30))
            if library_lst[i] == "  Videos":
                pushbuton.setIcon(QIcon("assets/resources/images/movie25.png"))
                pushbuton.setIconSize(QSize(30, 30))
            if library_lst[i] == "  Documents":
                pushbuton.setIcon(QIcon("assets/resources/images/documents25.png"))
                pushbuton.setIconSize(QSize(30, 30))

            pushbuton.setStyleSheet("""
            QPushButton{
            color: white;
            background: transparent;
            background-color : rgba(255, 255  ,255 ,20);
            margin: 2px;
            border-radius: 7px;
            }
            
            QPushButton::hover{
            color: white;
            background-color : rgba(255, 255  ,255 ,30);
            border-radius: 7px;
            
            }
            
            QPushButton::pressed{
            background-color: rgba(255, 255, 255, 50)
            }
            """)
            self.library_layout.addWidget(pushbuton, 0, i)

        drives = GetLogicalDriveStrings()
        lst = []
        for i in drives:
            if str(i).isalpha():
                lst.append("  " + i)

        for i in range(len(lst)):
            pushbuton = QPushButton(f"{lst[i]}")
            pushbuton.setMinimumSize(150, 90)
            # pushbuton.setMaximumSize(200, 150)

            pushbuton.setFont(QFont("Segoe UI", 16))

            # if library_lst[i] == "  Downloads":
            #     pushbuton.setIcon(QIcon("assets/resources/images/downloads.png"))
            #     pushbuton.setIconSize(QSize(25, 25))
            # if library_lst[i] == "  Music":
            #     pushbuton.setIcon(QIcon("assets/resources/images/music25.png"))
            #     pushbuton.setIconSize(QSize(45, 45))
            # if library_lst[i] == "  Pictures":
            #     pushbuton.setIcon(QIcon("assets/resources/images/picture25.png"))
            #     pushbuton.setIconSize(QSize(30, 30))
            # if library_lst[i] == "  Videos":
            #     pushbuton.setIcon(QIcon("assets/resources/images/movie25.png"))
            #     pushbuton.setIconSize(QSize(30, 30))
            # if library_lst[i] == "  Documents":
            #     pushbuton.setIcon(QIcon("assets/resources/images/documents25.png"))
            #     pushbuton.setIconSize(QSize(30, 30))

            pushbuton.setStyleSheet("""
            QPushButton{
            color: white;
            background: transparent;
            background-color : rgba(255, 255  ,255 ,20);
            margin: 3px;
            
            border-radius: 7px;
            }

            QPushButton::hover{
            color: white;
            background-color : rgba(255, 255  ,255 ,30);
            border-radius: 7px;

            }

            QPushButton::pressed{
            background-color: rgba(255, 255, 255, 50)
            }
            """)
            self.drives_layout.addWidget(pushbuton, 0, i)

    # ************************* MUSIC ***************************** #

    def music_indexer(self, *args):
        from random import choice
        # provide te choice
        t = ('Please wait while we take care of few things.', 'Indexing will help to search entire drive faster.',
             'Some changes have been found since last run. Please wait while we index.')

        def toast_r():
            # show toast
            try:
                ToastNotifier().show_toast(title='Indexing Musics in Local Drives.',
                                           msg=choice(t),
                                           duration=7,
                                           icon_path='Graphics/Elements/icon.ico')
            except (AttributeError, RuntimeError, AssertionError):
                pass

        Thread(target=toast_r).start()

        # def assist():
        #     try:
        #         loader = MP3("Assist/indexing.mp3")
        #         mixer.init(frequency=loader.info.sample_rate)
        #         mixer.music.load("Assist/indexing.mp3")
        #         mixer.music.play()
        #     except error:
        #         pass
        #     except Exception:
        #         pass
        #
        # Thread(target=assist).start()

        # main indexer to find the mp3 file
        musics = open(f'C:/Users/{GetUserName()}/AppData/Local/Temp/CachedData/mr.tru', 'w')
        path = open(f'C:/Users/{GetUserName()}/AppData/Local/Temp/CachedData/mp.tru', 'w')

        # walker
        for v in os.walk(r'C:/Users'):
            for g in v[2]:
                try:
                    if g.endswith('.mp3'):
                        musics.write(f'{g}\n')
                        path.write(f'{v[0]}\n')
                except UnicodeEncodeError:
                    pass

        new_songs = 0
        # # new drive walker
        # for i in range(current_active - 1):
        #     for e in get_active_drives[1:current_active]:
        #         walker_drives = os.walk(f'{e}')
        #         for z in walker_drives:
        #             for r in z[2]:
        #                 try:
        #                     if r.endswith('.mp3'):
        #                         f.write(f'{r}\n')
        #                         reviser.write(f'{z[0]}\n')
        #                         new_songs += 1
        #                 except UnicodeEncodeError:
        #                     pass
        # save and close the file
        musics.close()
        path.close()

        # with open('Asse', 'w') as ne:
        #     ne.write('False')

        # with open(f'C:/Users/{GetUserName()}/Fluent Player+/temp/Assets/optimizer.tru', "r") as optimize:
        #     reader = optimize.read()
        #
        # if reader == "True":
        #     try:
        #         ToastNotifier().show_toast(title=f"Added {new_songs} songs into library.",
        #                                    msg=f"We have found {new_songs} in your device and added to library. ",
        #                                    duration=14,
        #                                    icon_path="Graphics/Elements/icon.ico")
        #     except (RuntimeError, AttributeError, AssertionError):
        #         pass
        with open(f'C:/Users/{GetUserName()}/AppData/Local/Temp/CachedData/optimizer.tru', "w") as optimization:
            optimization.write("False")

    def music_handler(self, user_search=''):
        opener = open(f'C:/Users/{GetUserName()}/AppData/Local/Temp/CachedData/mp.tru', 'r')

        # read line by line
        reader = opener.readlines()
        # make a empty list say s
        s = []

        # set a int var to 0
        var = 0

        # iterate over the reader
        for z in reader:

            # if user search in the music or z then append s
            if user_search.title() in z or user_search.lower() in z or user_search.upper() in z:
                s.append(z[0:len(z) - 1])

                # search for only one song
                break

            # only one song is loaded therefore var = 1
            var += 1

        # make a new list
        next_list = []

        # append the items in the reader into next list
        for e in reader:
            # if user search is in e then append next list
            if user_search.title() in e:
                next_list.append(e)

        # make a clone of the net list
        clone = next_list[1:]

        # iterate over the clone
        for i in clone:
            # and save the content in the clone into a file
            with open(f'C:/Users/{GetUserName()}/AppData/Local/Temp/CachedData/Searched.tru', 'wb') as writer:
                writer.write(i.encode())

        # close the opened file
        opener.close()
        path_opener = open(f'C:/Users/{GetUserName()}/AppData/Local/Temp/CachedData/mp.tru', 'r')

        # new list
        lst = []

        # since only one song is located iterate and filter the song (remove living part say extension .mp3)
        for i in range(var + 1):
            reader_var = path_opener.readline()
            lst.append(str(reader_var))

        # filtering list
        new_lst = []

        # new list for values
        for i in lst:
            value = (len(i) - 1)
            new_lst.append(i[0:value])

        # finally load the song in to the memory and play it
        try:
            # get the length of the song
            loader = MP3(f'{new_lst[-1]}/{s[0]}')

            mixer.init(frequency=loader.info.sample_rate)

            frequency = loader.info.sample_rate

            with open(f'C:/Users/{GetUserName()}/AppData/Local/Temp/CachedData/Frequency.tru', 'w') as frequen:
                frequen.write(str(frequency))

            # load into memory
            mixer.music.load(f'{new_lst[-1]}/{s[0]}')

            # start playing thread
            mixer.music.play()

            # which song is playing
            current = s[0]

            # length of the song
            length = loader.info.length

            # from kivy.clock import Clock
            # def pos_save(*args):
            #     # pos
            #     file_pos = open(f'C:/Users/{GetUserName()}/Fluent Player+/temp/Assets/Preferences/pos.tru', "w")
            #     pos = mixer.music.get_pos()
            #     file_pos.write(str(pos))
            #     file_pos.close()
            #
            # Clock.schedule_interval(pos_save, 3.0)

            # return the values if playing song then return true, which song and its length
            return True, current, str(length)

        except (IndexError, HeaderNotFoundError, error, FileNotFoundError):
            pass
        except MutagenError:
            Thread(target=self.music_indexer).start()

    def music_UI(self):
        if not os.path.isfile(f'C:/Users/{GetUserName()}/AppData/Local/Temp/CachedData/mr.tru'):
            self.music_indexer()

        read_music = open(f'C:/Users/{GetUserName()}/AppData/Local/Temp/CachedData/mr.tru', 'r').readlines()
        val = 0
        for z in read_music:
            songs_button = QPushButton()
            songs_button.setMaximumHeight(35)
            songs_button.setFont(QFont('Yu Gothic UI', 9))
            # songs_button.clicked.connect(self.music_handler(user_search=str(z)))
            songs_button.setStyleSheet("""
            QPushButton{
                color: white;
                background: transparent;
                text-align: left;	
                padding-left: 10px;
                }
                
                QPushButton::hover{
                    color: white;
                    background-color : rgba(255, 255  ,255 ,50);
                
                }
                
                QPushButton::pressed{
                    background-color: rgba(255, 255, 255, 80)
                }

            """)
            self.songs_layout.addWidget(songs_button)
            val += 1

    def clear_search(self):
        self.search_box.setText('')

    def downloads_UI(self):
        QtWidgets.QTabWidget.setCurrentIndex(self.tabWidget, 1)

    def feedback_UI(self):
        # self.slideMenu(True)
        self.stackedWidget.setCurrentIndex(2)

    def remove_feedback_graphics(self):
        feedback_blur_remove = QGraphicsBlurEffect()
        feedback_blur_remove.setBlurRadius(0.0)
        settings_blur_remove = QGraphicsBlurEffect()
        settings_blur_remove.setBlurRadius(0.0)
        self.feedback_graphics_frame.setGraphicsEffect(feedback_blur_remove)
        self.settings_3.setGraphicsEffect(settings_blur_remove)
        self.write_to_us.setText(" Write to us.")
        self.write_to_us_box.setPlainText("")
        self.settings_3.setEnabled(True)

    def feedback_graphics_effect_UI(self):
        feedback_frame_blur = QGraphicsBlurEffect()
        feedback_frame_blur.setBlurRadius(15.0)
        settings_frame_blur = QGraphicsBlurEffect()
        settings_frame_blur.setBlurRadius(15.0)
        self.write_to_us_box.setPlainText("         Write Here")
        # self.setBlurRadius(15.0)
        self.feedback_graphics_frame.setGraphicsEffect(feedback_frame_blur)
        self.settings_3.setGraphicsEffect(settings_frame_blur)
        self.settings_3.setDisabled(True)
        self.write_to_us.setVisible(False)
        self.write_to_us_box.setEnabled(True)
        self.send_feedback.setVisible(True)
        self.response.setVisible(False)
        self.sent_ui.setVisible(False)
        self.send_feedback.clicked.connect(self.compose_email)

    def compose_email(self):

        if connection():
            self.sent_ui.setVisible(True)
            self.response.setVisible(True)
            self.write_to_us_box.setVisible(False)
            self.sent_ui.setIcon(QIcon('assets/resources/images/mark96.png'))
            self.sent_ui.setIconSize(QSize(96, 96))
            self.remove_feedback_graphics()
            self.write_to_us.setVisible(False)
            self.write_to_us_box.setEnabled(False)
            self.send_feedback.setVisible(False)
        else:
            self.sent_ui.setVisible(True)
            self.response.setVisible(True)
            self.remove_feedback_graphics()
            self.response.setText('Not connected to the internet.')
            self.write_to_us_box.setVisible(False)
            self.sent_ui.setIcon(QIcon('assets/resources/images/cross96.png'))
            self.sent_ui.setIconSize(QSize(96, 96))

            self.write_to_us.setVisible(True)
            self.send_feedback.setVisible(False)

    def appearance_UI(self):
        self.stackedWidget.setCurrentIndex(0)

    def functionalities(self):
        self.feedback.clicked.connect(self.feedback_UI)
        self.write_to_us.clicked.connect(self.feedback_graphics_effect_UI)
        # Title bar buttons
        self.music.clicked.connect(self.music_UI)
        self.minimize.clicked.connect(self.min)
        self.maximize.clicked.connect(self.max_reduce)
        self.collapse.clicked.connect(self.menu_handler)
        self.close.clicked.connect(self.stop)
        self.thisPC.clicked.connect(self.thisPC_UI)
        # self.search_clear.clicked.connect(self.clear_search)
        self.downloads.clicked.connect(self.downloads_UI)
        self.effect_radiobutton.toggled.connect(self.setup_elegantUi)
        self.theme_box.activated.connect(self.theme_manager)
        self.appearance.clicked.connect(self.appearance_UI)
        self.startup.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

        # starup
        self.specific_page.toggled.connect(lambda: self.specific_page_url.setEnabled(True))
        self.left_off.toggled.connect(lambda: self.specific_page_url.setEnabled(False))
        self.new_tab_toggle.toggled.connect(lambda: self.specific_page_url.setEnabled(False))

    def themeRegistry(self, theme='acrylic'):
        with open('rep32.dll', 'w') as theme_writer:
            theme_writer.write(theme)

    def setTheme(self, theme= 'dark'):
        with open('rep32.dll', 'r') as reader:
            read = reader.read()

        if read == 'dark':
            self.set_acrylic(False, 'dark')
        elif read == 'amoled' or theme == 'amoled':
            self.set_acrylic(False, 'amoled')
        elif read == 'acrylic' or theme == 'acrylic':
            if self.effect_radiobutton.isChecked():
                self.set_acrylic(True, 'set_all')
            else:
                self.set_acrylic(True, 'set_on_left')
        elif read == 'blur' or theme == 'blur':
            if self.effect_radiobutton.isChecked():
                self.set_acrylic(True, 'set_all')
            else:
                self.set_acrylic(True, 'set_on_left')
        elif read == 'default':
            self.set_acrylic(True, 'default')
        elif read == 'transparent' or theme == 'transparent':
            self.set_acrylic(False, 'semi-transparent')

    def theme_manager(self):

        if self.theme_box.currentText() == 'Dark':
            self.set_acrylic(False, 'dark')
            self.themeRegistry('dark')
            self.additional_settings_manager('set_invisible')

        elif self.theme_box.currentText() == 'Blur':
            with open('effectSupport.dll', 'w') as writer:
                writer.write('ten')
            self.themeRegistry('blur')
            self.additional_settings_manager('set_visible')

            with open("assets/resources/holder.tru", 'r') as val:
                    r = val.read()
            # Frame One UI
            frame_one_image = Image.open(f'C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_ref{r}.jpeg')
            skinned_ = Image.eval(frame_one_image, lambda x: x / 2.2)

            frame_one_blurred_image = skinned_.filter(GaussianBlur(radius=10))
            frame_one_blurred_image.save(f"C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_rea.jpeg")

            if self.effect_radiobutton.isChecked():
                self.set_acrylic(False, 'transparent')
                self.all_frame.setStyleSheet(f"""
                    background: url('C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_rea.jpeg');
                    background-repeat: no-repeat;
                    background-position: left;
                    border: 0;""")
            else:
                self.set_acrylic(False, 'amoled')
                self.graphics.setStyleSheet(f"""
                    
                    background: url('C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_rea.jpeg');
                    background-repeat: no-repeat;
                    background-position: left;
                    border: 0;""")

        elif self.theme_box.currentText() == 'Default':
            self.additional_settings_manager('set_invisible')
            self.set_acrylic(True, 'set_on_left')
            self.themeRegistry('default')

        elif self.theme_box.currentText() == 'Amoled':
            self.additional_settings_manager('set_invisible')
            self.set_acrylic(False, 'amoled')
            self.themeRegistry('amoled')

        elif self.theme_box.currentText() == 'Acrylic':
            self.additional_settings_manager('set_invisible')
            with open('effectSupport.dll', 'w') as writer:
                writer.write('acrylic')
            with open("assets/resources/holder.tru", 'r') as val:
                r = val.read()
            # Frame One UI
            frame_one_image = Image.open(f'C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_ref{r}.jpeg')
            skinned_ = Image.eval(frame_one_image, lambda x: x / 2.2)

            frame_one_blurred_image = skinned_.filter(GaussianBlur(radius=35))
            frame_one_blurred_image.save(f"C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_rea.jpeg")

            if self.effect_radiobutton.isChecked():
                self.set_acrylic(False, 'transparent')
                self.all_frame.setStyleSheet(f"""
                    background: url('C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_rea.jpeg');
                    background-repeat: no-repeat;
                    background-position: left;
                    border: 0;""")
            else:
                self.set_acrylic(False, 'amoled')
                self.graphics.setStyleSheet(f"""
                    
                    background: url('C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_rea.jpeg');
                    background-repeat: no-repeat;
                    background-position: left;
                    border: 0;""")

            self.themeRegistry('acrylic')
        elif self.theme_box.currentText() == 'Transparent':
            self.themeRegistry('transparent')
            self.set_acrylic(False, 'semi-transparent')
            self.additional_settings_manager('tint_only')

        elif self.theme_box.currentText() == 'Light':
            self.themeRegistry('light')
            self.set_acrylic(False, 'light')

def switch_check():
    writer =  open("config.dll", "w")
    if keyboard.is_pressed("alt"):
        writer.write("False")
    elif keyboard.read_key() == 'left windows':
        writer.write('False')
        print('window set up')
    else:
        writer.write("True")

    print('Checking switch..')
    writer.close()

# @ staticmethod
def check_window():
    try:
        # get the current active window
        a = pygetwindow.getActiveWindowTitle()

        if str(a) != "Fluent Explorer.exe":
            try:

                # minimize
                MainWindow.showMinimized()

                with open("config.dll", "r") as reader:
                    read_config = reader.read()

                with open('DWM.dll', 'w') as writer:
                    writer.write('True')

                # mouse reader
                # with open('assets/abstracts/meta.dll', 'r') as reader:
                #     rp = reader.read()

                # grab screen
                if read_config == "True" or read_config == '':
                    get_image = screenshot()
                    print('Using Brush..')

                    # random value grabber
                    r = str(randint(10, 100000))

                    # save value into a file for furure use   this is the fool
                    with open("assets/resources/holder.tru", 'w') as hold:
                        hold.write(r)

                    # save at this location thi
                    get_image.save(f'C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_ref{r}.jpeg')

                with open("assets/resources/holder.tru", 'r') as val:
                    r = val.read()
                # Frame One UI
                frame_one_image = Image.open(f'C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_ref{r}.jpeg')

                with open('effectSupport.dll', 'r') as reader:
                    read = reader.read()

                if read ==  'ten':
                    func = lambda x: x/3.0
                else:
                    func = lambda x: x/3.5

                skinned_ = Image.eval(frame_one_image, func)
                # blur the image


                if read == 'ten':
                    radii = 10
                else:
                    radii = 50

                frame_one_blurred_image = skinned_.filter(GaussianBlur(radius=radii))
                frame_one_blurred_image.save(f"C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_reb1{r}.jpeg")

                with open("assets/resources/qr.tru", "r") as reader:
                    read = str(reader.read())

                if read == "True":
                    with open("lib.dll", "r") as reader:
                        read = str(reader.read())

                    if read == "True":
                        # MainWindow.set_acrylic(True, "set_all")
                        MainWindow.setTheme()
                    else:
                        # MainWindow.set_acrylic(True, "set_on_left")
                        MainWindow.setTheme()
                    with open("assets/resources/qr.tru", "w") as writer:
                        writer.write("False")


            # will raise OS error if imaghow to add padding in pushbutton icon in pyqte is subjected to modifications
            except OSError:
                pass

        elif MainWindow.isMaximized():
            MainWindow.setWindowOpacity(1.0)

            # FRAMES UI

            # FRAME 1
            with open("assets/resources/qr.tru", "r") as reader:
                read = str(reader.read())

            if read == "True":
                with open("lib.dll", "r") as reader:
                    read = str(reader.read())

                if read == "True":
                    # MainWindow.set_acrylic(True, "set_all")
                    MainWindow.setTheme()
                else:
                    # MainWindow.set_acrylic(True, "set_on_left")
                    MainWindow.setTheme()
                with open("assets/resources/qr.tru", "w") as writer:
                    writer.write("False")


        else:

            with open('DWM.dll', 'r') as reader:
                read_n = reader.read()

            # with open('rep32.dll', 'r') as reader:
            #     read = reader.read()

            if read_n == 'True':
                # if read == 'acrylic':
                #     MainWindow.setTheme(read)
                # elif read == 'dark':
                #     MainWindow.setTheme(read)
                # else:
                #     MainWindow.all_frame.setStyleSheet(f"""background: black;""")
                #     MainWindow.window_frame.setStyleSheet(f"""background: black;""")
                #     MainWindow.graphics.setStyleSheet(f"""background: black;""")
                #     MainWindow.showMinimized()
                #     MainWindow.showMaximized()

                MainWindow.setTheme()

            with open('DWM.dll', 'w') as writer:
                writer.write('False')

    except NameError:
        pass


def no_screen():
    current = pygetwindow.getActiveWindowTitle()
    if MainWindow.isMinimized() or current != "Fluent Explorer.exe" or not MainWindow.isMaximized():
        with open("assets/resources/block.tru", "w") as writer:
            writer.write("True")
        with open("assets/resources/qr.tru", "w") as writer:
            writer.write("True")
    if MainWindow.isMaximized():
        with open("assets/resources/block.tru", 'r') as reader:
            read = str(reader.read())
        if read == "True":
            MainWindow.fluentHandler()
            with open("assets/resources/block.tru", "w") as writer:
                writer.write("False")
    if MainWindow.isMinimized() or current != "Fluent Explorer.exe":
        with open("assets/resources/QtS.dll", "w") as writer:
            writer.write("True")
    # if not MainWindow.isMaximized():
    #     with open("assets/resources/QtS.dll", "r") as reader:
    #         read = str(reader.read())
    #     if read == "True":
    #         MainWindow.setStyleSheet("""background-color: black;""")
    #         MainWindow.graphics.setStyleSheet("""background-color: black;""")


def cleaner():
    a = pygetwindow.getActiveWindowTitle()

    if str(a) != "Fluent Explorer.exe":
        walker = os.walk(f'C:/Users/{USER}/AppData/Local/Temp/CachedData/cache')

        for i in walker:
            r = i[2]
            for g in r:
                if g.endswith('.jpeg'):
                    with open(f'assets/resources/holder.tru', "r") as t:
                        ri = str(t.read())
                    if ri in str(g):
                        pass
                    else:
                        z = g
                        try:
                            os.remove(f"C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/{z}")
                        except (PermissionError, FileNotFoundError):
                            pass


def clock(func, sec):
    def wrapper():
        clock(func, sec)
        func()

    t = Timer(sec, wrapper)
    try:
        t.start()
    except RuntimeError:
        pass


clock(cleaner, 1.0)
clock(switch_check, 0.2)


app = QApplication(sys.argv)
MainWindow = Main()
windowTimer = QTimer()
windowTimer.timeout.connect(no_screen)
windowTimer.timeout.connect(check_window)
windowTimer.setInterval(1)
windowTimer.start()
MainWindow.show()
start_splash()
app.exec()




