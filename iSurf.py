from random import randint
from threading import Thread, Timer
import pygetwindow
from PIL import Image  # pip install pillow
from PIL.ImageFilter import *
from PyQt5.QtCore import *  # pip install PyQt5
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *  # search for it
from PyQt5.QtWidgets import *
from pyautogui import *
from win32api import *
from win10toast import ToastNotifier
import keyboard
from PyQt5 import QtWidgets, QtCore, QtGui, uic
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

        # # UI Setup
        self.ui = uic.loadUi("D:/file_explorer_ui/UPDATE4.ui", self)
        self.show()

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

        if read_theme == 'acrylic':
            self.theme_box.setCurrentIndex(1)
        elif read_theme == 'transparent':
            self.theme_box.setCurrentIndex(2)
        elif read_theme == 'blur':
            self.theme_box.setCurrentIndex(3)
        elif read_theme == 'light':
            self.theme_box.setCurrentIndex(4)
        elif read_theme == 'dark':
            self.theme_box.setCurrentIndex(5)
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
                self.set_acrylic(True, "set_all")
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
        else:
            self.showMaximized()
            icon = QIcon()
            icon.addFile("assets/resources/images/estore.png", QSize(), QIcon.Normal, QIcon.Off)
            self.maximize.setIcon(icon)
            self.set_acrylic(True)

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
        # self.close.clicked.connect(self.stop)
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

        elif self.theme_box.currentText() == 'Blur':
            with open('effectSupport.dll', 'w') as writer:
                writer.write('ten')
            self.themeRegistry('blur')

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
            self.set_acrylic(True, 'set_on_left')
            self.themeRegistry('default')

        elif self.theme_box.currentText() == 'Amoled':
            self.set_acrylic(False, 'amoled')
            self.themeRegistry('amoled')

        elif self.theme_box.currentText() == 'Acrylic':
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
                    func = lambda x: x/4.0

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
# clock(no_screen, 0.1)


if __name__ == '__main__':
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




