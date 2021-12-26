import sys 
from PyQt5 import QtWidgets
from asistanForm import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolTip, QGraphicsDropShadowEffect
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore 
from PyQt5.QtGui import QCursor, QWindow, QMovie
from voice import *
import time as tt
from PyQt5.QtCore import Qt

class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.butonMic.clicked.connect(self.startAsistant)

        self.ui.closeButton.clicked.connect(self.closeScreen)

        self.ui.minimizeButton.clicked.connect(self.minimizeScreen)

        self.ui.sideBarButton.clicked.connect(self.sideBar)   
    
        self.ui.sideBarLabel.setHidden(True)

        self.ui.sideHiddenButton.clicked.connect(self.sideBarHidden)

        self.ui.sideHiddenButton.setHidden(True)

        self.ui.informationLabel.setHidden(True)

        self.ui.movie = QMovie("tenor2.gif")
        self.ui.gifLabel.setMovie(self.ui.movie)
        self.ui.gifLabel.setScaledContents(True)
        self.ui.gifLabel.setHidden(True)
        self.ui.movie.start()

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(75)
        shadow.setColor(Qt.black)
        
        self.ui.sideBarLabel.setGraphicsEffect(shadow)

        shadow_two = QGraphicsDropShadowEffect()
        shadow_two.setBlurRadius(75)
        shadow_two.setColor(Qt.black)
        self.ui.gifLabel.setGraphicsEffect(shadow_two)
           
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moveFlag = True
            self.movePosition = event.globalPos() - self.pos()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            event.accept()
            
    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.moveFlag:
            
            self.move(event.globalPos() - self.movePosition)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.moveFlag = False
        self.setCursor(Qt.ArrowCursor)
    
    def startAsistant(self):
        getvoices(1)
        #wishme()
        wakeword = 'bumblebee' # Assistan name. 

        while True:

            query = takeCommandMIC().lower()

            getSounder = "" + query

            #if wakeword in getSounder:
            self.ui.micLabel.setText(f"{getSounder}")
            QtWidgets.qApp.processEvents()

            query = word_tokenize(query)
            print(query)

            if wakeword in query:

                if 'time' in query:
                    self.ui.resultLebel.setText(f" {timeStr()}")
                    QtWidgets.qApp.processEvents()
                    degisken =""+ timeStr()
                    speak(degisken)
                    
                elif 'date' in query:
                    self.ui.resultLebel.setText(f" {dateStr()}")
                    QtWidgets.qApp.processEvents()
                    degisken = ""+ dateStr()
                    speak(degisken)

                elif 'email' in query:     
                    while True:
                        try:
                            self.ui.resultLebel.setText('Select a e-mail type:<br>gmail - hotmail - yahoo')
                            QtWidgets.qApp.processEvents()
                            speak('Select a e-mail type:')
                            a = takeCommandMIC().lower()
                            print(a)
                            if 'gmail' in a:
                                b = '@gmail.com'
                            elif 'hotmail' in a:
                                b = '@hotmail.com'
                            elif 'yahoo' in a:
                                b = '@yahoo.com'
                            else:
                                print ('Unavaliable e-mail type!')
                                continue

                            if '@gmail.com' == b or '@hotmail.com' == b or '@yahoo.com' == b:
                                speak("\nTo whom will the e-mail be sent? ")
                                m = takeCommandMIC().lower().replace(' ','')
                                receiver = m + b
                                self.ui.resultLebel.setText(receiver + ' is it true? If mail true say yes else say no: ')
                                QtWidgets.qApp.processEvents()
                                print(receiver + ' is it true? If mail true say yes else say no: ')
                                speak(receiver + ' is it true? If mail true say yes else say no: ')
                                check_mail = takeCommandMIC().lower()

                                if "yes" in check_mail:
                                    print('\nWhat is the subject of the mail?\nSubject:')
                                    speak('\nWhat is the subject of the mail?')
                                    subject = takeCommandMIC()
                                        
                                    print('\nWhat should I say?\nContent: ')
                                    speak('\nWhat should I say?')
                                    content = takeCommandMIC()
                                    sendEmail(receiver, subject, content)
                                    self.ui.resultLebel.setText(receiver + '<br>E-mail has been succesfully send.')
                                    QtWidgets.qApp.processEvents()
                                    print('\nE-mail has been succesfully send.')
                                    break
                                    
                                elif 'no' in check_mail:
                                    print('Try again to say yes else no: ')
                                    speak('Try again to say yes else no: ')
                                    question = takeCommandMIC().lower()
                                    if 'yes' in question:
                                        print('yes')
                                        pass                       
                                    elif 'no' in question:
                                        print('no')
                                        break
                                    else:
                                        speak('Unavaliable command')
                                        print('Unavaliable command')
                                        break
                            else:
                                continue
                        except:
                            print('Error')
            
                elif 'message' in query:

                    while True:
                        try: 
                            speak("To whom you want to send the whatsapp message? Please say receiver phone number")
                            phone_no = '+905' + takeCommandMIC().replace(' ','')
                            print(phone_no)
                            self.ui.resultLebel.setText(phone_no)
                            QtWidgets.qApp.processEvents
                            speak('Is it true phone number?')
                            number_check = takeCommandMIC()
                            if 'yes' in number_check:
                                speak('What is the message?')
                                message = takeCommandMIC()
                                sendwhatsappmsg(phone_no, message.replace(' ','+'))
                                self.ui.resultLebel.setText(""+phone_no+"<br>"+message+"<br>Message has been succesfully send.")
                                QtWidgets.qApp.processEvents
                                print('Message has been succesfully send.')
                                break
                            elif 'no' in number_check:
                                speak('Try again?')
                                question = takeCommandMIC()
                                if 'yes' in question:
                                    pass
                                elif 'no' in question:
                                    break
                                else:
                                    speak('Unavalibale command!')
                                    break
                            else:
                                speak('Unavalibale command!')
                                break

                        except Exception:
                            print('Unable to send the message!')
                            self.ui.resultLebel.setText('Unable to send the message!')
                            QtWidgets.qApp.processEvents

                elif 'wikipedia' in query:
                    speak('What would you like to search on wikipedia?')
                    try:
                        wiki_search = takeCommandMIC()
                        speak('Searching on wikipedia...')
                        result = wikipedia.summary(wiki_search, sentences = 2)
                        print(result)
                        self.ui.resultLebel.setText(result)
                        QtWidgets.qApp.processEvents()
                        speak(result)
                    except:
                        speak(f'Sorry {wiki_search} unavaliale on wikipedia.')
                    
                elif 'search' in query:
                    self.ui.resultLebel.setText("will be searched on google for you...")
                    QtWidgets.qApp.processEvents()
                    searchgoogle()

                elif 'youtube' in query:
                    try:
                        speak('What should I search for on youtube?')
                        topic = takeCommandMIC()
                        pywhatkit.playonyt(topic)
                        self.ui.resultLebel.setText(f"{topic} will be played!")
                        QtWidgets.qApp.processEvents()
                    except:
                        self.ui.resultLebel.setText("Sorry, we don't find your video in YouTube.")
                        QtWidgets.qApp.processEvents()

                elif 'weather' in query:
                    speak('Pleasee say a city name: ')
                    cityName = ""+ takeCommandMIC()
                    cityName.lower()

                    cityName = weatherStr(cityName)

                    self.ui.resultLebel.setText(cityName)
                    QtWidgets.qApp.processEvents()

                elif 'news' in query:
                    self.ui.resultLebel.setText(news())
                    QtWidgets.qApp.processEvents()
                  
                elif 'read' in query:
                    try:
                        result = texttospeech()
                        self.ui.resultLebel.setText(result)
                        QtWidgets.qApp.processEvents()
                        speak(result)
                    except:
                        self.ui.resultLebel.setText('Sorry, your clipboard is empty please copy anything.')
                        QtWidgets.qApp.processEvents()

                elif 'covid-19' in query:
                    result = covid()
                    self.ui.resultLebel.setText(result)
                    QtWidgets.qApp.processEvents()
                    #speak(result)
                                  
                elif 'open' in query:
                    try:
                        os.system('explorer C://{}'.format(query.replace('Open', '')))
                    except:
                        self.ui.resultLebel.setText('Sorry, this file or folder not available in directory.')
                        QtWidgets.qApp.processEvents()

                elif 'joke' in query:
                    result = pyjokes.get_joke()
                    self.ui.resultLebel.setText(result)
                    QtWidgets.qApp.processEvents()
                    speak(result) 

                elif 'screenshot' in query:
                    try:
                        #D:\sesli_asistan_2.dönem_proje\asistan_deneme_5\
                        result = screenshotStr()
                        pixmap = ""+result+".png"
                        pixmap_two = QPixmap(pixmap)
                        print(pixmap)
                        self.ui.resultLebel.setPixmap(pixmap_two)
                        self.ui.resultLebel.setScaledContents(True)
                        #self.resize(pixmap.width(),pixmap.height()
                        QtWidgets.qApp.processEvents()
                    except:
                        self.ui.resultLebel.setText('Sorry, we encountered an unexpected error.')
                        QtWidgets.qApp.processEvents()

                elif 'remember' in query:
                    speak('What should I remember for you?')
                    data = takeCommandMIC()
                    speak('You said me to remember that' + data)
                    self.ui.resultLebel.setText('You said me to remember that:<br><br>' + data)
                    QtWidgets.qApp.processEvents()
                    remember = open('data.txt','a')
                    remember.write(data)
                    remember.close()

                elif 'notebook' in query:
                    remember = open('data.txt','r')
                    result = remember.read()
                    self.ui.resultLebel.setText(result)
                    QtWidgets.qApp.processEvents()
                    speak('You told me to emember that' + remember.read())

                elif 'password' in query:
                    result = passwordgen()
                    self.ui.resultLebel.setText(result)
                    QtWidgets.qApp.processEvents()
                    speak(result)       

                elif 'discord' in query:
                    try:
                        self.ui.resultLebel.setText("Visual Studio will be open!")
                        QtWidgets.qApp.processEvents()
                        codepath = 'C:\\Users\\USER\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Discord Inc\\Discord'                    
                        os.startfile(codepath)
                    except:
                        self.ui.resultLebel.setText('Sorry, application not found in your device.')
                        QtWidgets.qApp.processEvents()
               
                elif 'flip' in query:
                    result = flipcoin()
                    self.ui.resultLebel.setText(result)
                    QtWidgets.qApp.processEvents()
                    speak(result)          
                    
                elif 'roll' in query:
                    result = roll()
                    self.ui.resultLebel.setText(result)
                    QtWidgets.qApp.processEvents()
                    speak(result)

                elif 'cpu' in query:
                    result = cpuStr()
                    self.ui.resultLebel.setText(result)
                    QtWidgets.qApp.processEvents()
                    speak(result.replace('<br>',' '))
                    
                elif 'film' in query:
                    result = imdb()
                    self.ui.resultLebel.setText(result)
                    QtWidgets.qApp.processEvents()

                elif 'location' in query:
                    try:
                        result = location()
                        self.ui.resultLebel.setText(result)
                        QtWidgets.qApp.processEvents()
                        speak(result)
                    except:
                        self.ui.resultLebel.setText('Sorry, we were unable to locate your location. Please try again by turning on the location feature of your device.')
                        QtWidgets.qApp.processEvents()
                        speak('Sorry, we were unable to locate your location. Please try again by turning on the location feature of your device.')

                elif 'currency' in query:
                    result = dolar()+"<br><br>" + euro()
                    self.ui.resultLebel.setText(result)
                    QtWidgets.qApp.processEvents()
                    speak(result.replace("br",""))

                elif 'goodbye' in query:
                    self.ui.resultLebel.setText('Goodbye!')
                    QtWidgets.qApp.processEvents()
                    speak("Goodbye!")
                    break
        
    def closeScreen(self):
        quit()

    def minimizeScreen(self):
        self.ui.sideBarButton.setHidden(False)
        self.ui.sideHiddenButton.setHidden(True)
        self.ui.informationLabel.setHidden(True)
        self.ui.sideBarLabel.setHidden(True)
        self.ui.gifLabel.setHidden(True)
        self.showMinimized()
    
    def sideBar(self):
        self.ui.sideBarLabel.setHidden(False)
        self.ui.gifLabel.setHidden(False)
        self.ui.informationLabel.setHidden(False)
        self.ui.sideHiddenButton.setHidden(False)
        self.ui.sideBarButton.setHidden(True)
               
    def sideBarHidden(self):
        self.ui.sideBarButton.setHidden(False)
        self.ui.sideHiddenButton.setHidden(True)
        self.ui.sideBarLabel.setHidden(True)
        self.ui.gifLabel.setHidden(True)
        self.ui.informationLabel.setHidden(True)

def app():
    app = QtWidgets.QApplication(sys.argv)
    win = Window()

    win.setWindowFlag(QtCore.Qt.FramelessWindowHint)

    win.show()
    sys.exit(app.exec_())

app()