class ThemeHandler:

    def __init__(self, MainWindow):
        global main_color, rgb
        with open('rep32.dll', 'r') as reader:
            read = reader.read()

        if read == 'light':
            rgb = 'rgb(255, 255, 255)'
            main_color = 'white'
        elif read != 'light':
            rgb = 'rgb(0, 0, 0)'
            main_color = 'black'

        MainWindow.all_frame.setStyleSheet(f"""background-color: {rgb};""")
        MainWindow.window_frame.setStyleSheet(f"""background-color: {rgb};""")
        MainWindow.graphics.setStyleSheet(f"""background-color: {rgb};""")
        MainWindow.appearance.setStyleSheet(f'''
        QPushButton{
            f'color: {main_color};'
            'background: transparent;'
            'padding-left: 10px;'
            }
            
            QPushButton::hover{
                'background-color : rgba(0, 0  ,0 ,50);'
            } 
            QPushButton::pressed{
                'background-color: rgba(0, 0, 0, 80)'
            }
            ''')
        MainWindow.passwords.setStyleSheet('''
        QPushButton{
            color: black;
            background: transparent;
            padding-left: 10px;
            }

            QPushButton::hover{
                background-color : rgba(0, 0  ,0 ,50);
            } 
            QPushButton::pressed{
                background-color: rgba(0, 0, 0, 80)
            }
            ''')
        MainWindow.startup.setStyleSheet('''
        QPushButton{
            color: black;
            background: transparent;
            padding-left: 10px;
            }

            QPushButton::hover{
                background-color : rgba(0, 0  ,0 ,50);
            } 
            QPushButton::pressed{
                background-color: rgba(0, 0, 0, 80)
            }
            ''')
        MainWindow.controller.setStyleSheet('''
        QPushButton{
            color: black;
            background: transparent;
            padding-left: 10px;
            }

            QPushButton::hover{
                background-color : rgba(0, 0  ,0 ,50);
            } 
            QPushButton::pressed{
                background-color: rgba(0, 0, 0, 80)
            }
            ''')
        MainWindow.feedback.setStyleSheet('''
        QPushButton{
            color: black;
            background: transparent;
            padding-left: 10px;
            }

            QPushButton::hover{
                background-color : rgba(0, 0  ,0 ,50);
            } 
            QPushButton::pressed{
                background-color: rgba(0, 0, 0, 80)
            }
            ''')
        MainWindow.collapse.setStyleSheet('''
        QPushButton{
            color: black;
            background: transparent;
            padding-left: 10px;
            }

            QPushButton::hover{
                background-color : rgba(0, 0  ,0 ,50);
            } 
            QPushButton::pressed{
                background-color: rgba(0, 0, 0, 80)
            }
            ''')
        MainWindow.documents.setStyleSheet('''
            QPushButton{
            color: black;
            background: transparent;
            text-align: left;	
            padding-left: 10px;
            }
            
            QPushButton::hover{
            background-color : rgba(0, 0, 0 ,50);
            
            }
            
            QPushButton::pressed{
            background-color: rgba(0, 0, 0, 80)
            }

            ''')
        MainWindow.videos.setStyleSheet('''
                        QPushButton{
            color: black;
            background: transparent;
            text-align: left;	
            padding-left: 10px;
            }
            
            QPushButton::hover{
            background-color : rgba(0, 0, 0 ,50);
            
            }
            
            QPushButton::pressed{
            background-color: rgba(0, 0, 0, 80)
            }

            ''')
        MainWindow.pictures.setStyleSheet('''
                        QPushButton{
            color: black;
            background: transparent;
            text-align: left;	
            padding-left: 10px;
            }
            
            QPushButton::hover{
            background-color : rgba(0, 0, 0 ,50);
            
            }
            
            QPushButton::pressed{
            background-color: rgba(0, 0, 0, 80)
            }

            ''')
        MainWindow.music.setStyleSheet('''
                        QPushButton{
            color: black;
            background: transparent;
            text-align: left;	
            padding-left: 10px;
            }
            
            QPushButton::hover{
            background-color : rgba(0, 0, 0 ,50);
            
            }
            
            QPushButton::pressed{
            background-color: rgba(0, 0, 0, 80)
            }

            ''')
        MainWindow.downloads.setStyleSheet('''
                        QPushButton{
            color: black;
            background: transparent;
            text-align: left;	
            padding-left: 10px;
            }
            
            QPushButton::hover{
            background-color : rgba(0, 0, 0 ,50);
            
            }
            
            QPushButton::pressed{
            background-color: rgba(0, 0, 0, 80)
            }

            ''')
        MainWindow.thisPC.setStyleSheet('''
                       QPushButton{
            color: black;
            background: transparent;
            text-align: left;	
            padding-left: 10px;
            }
            
            QPushButton::hover{
            background-color : rgba(0, 0, 0 ,50);
            
            }
            
            QPushButton::pressed{
            background-color: rgba(0, 0, 0, 80)
            }

            ''')
        MainWindow.GDrive.setStyleSheet('''
                        QPushButton{
            color: black;
            background: transparent;
            text-align: left;	
            padding-left: 10px;
            }
            
            QPushButton::hover{
            background-color : rgba(0, 0, 0 ,50);
            
            }
            
            QPushButton::pressed{
            background-color: rgba(0, 0, 0, 80)
            }

            ''')
        MainWindow.settings.setStyleSheet('''
                        QPushButton{
            color: black;
            background: transparent;
            text-align: left;	
            padding-left: 10px;
            }

            QPushButton::hover{
            background-color : rgba(0, 0, 0 ,50);

            }

            QPushButton::pressed{
            background-color: rgba(0, 0, 0, 80)
            }

            ''')
        MainWindow.appearance.setStyleSheet('''
        QPushButton{
            color: black;
            background: transparent;
            padding-left: 10px;
            }
            
            QPushButton::hover{
                background-color : rgba(0, 0  ,0 ,50);
            } 
            QPushButton::pressed{
                background-color: rgba(0, 0, 0, 80)
            }
            ''')
        MainWindow.search_box.setStyleSheet(
            '''
            QLineEdit {
            color: black;
            border-radius: 5px;
            border: 2px solid rgb(91, 101, 124);
            padding-left: 10px;
            selection-color: rgb(0, 0, 0);
            selection-background-color: rgb(0, 121, 198);
            background: transparent;
            }
            
            QLineEdit:hover {
            border: 2px solid rgb(64, 71, 88);
            background-color: rgba(0, 0, 0, 30)
            }
            
            QLineEdit:focus {
            border: 2px solid rgb(91, 101, 124);
            }'''
        )
        MainWindow.path.setStyleSheet(
            '''
            QLineEdit {
            color: black;
            border-radius: 5px;
            border: 2px solid rgb(91, 101, 124);
            padding-left: 10px;
            selection-color: rgb(0, 0, 0);
            selection-background-color: rgb(0, 121, 198);
            background: transparent;
            }
            
            QLineEdit:hover {
            border: 2px solid rgb(64, 71, 88);
            background-color: rgba(0, 0, 0, 30)
            }
            
            QLineEdit:focus {
            border: 2px solid rgb(91, 101, 124);
            }
            ''')
