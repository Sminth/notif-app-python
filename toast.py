import sys
import os

import pyttsx3 
from PyQt5 import QtWidgets, uic
from PyQt5 import *
import sys,time
from PyQt5.QtWidgets import QMessageBox,qApp
import qtawesome as qta
#os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%
from toast_ui import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import threading, random
import pyperclip
import webbrowser,tempfile
class syncWorker(QObject):
    """class en parallele avec le programme principal
       chaque 30 minute elle communique au programme principale le message
       a afficher grace au pyqtSignal
    """
    setMess = pyqtSignal(str)
    def __init__(self):
       super().__init__()
 
    @pyqtSlot()
    def loop(self):
       while True:
           time.sleep(1800)
           self.setMess.emit("ok")

        


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        MainWindow.setWindowIcon(self,QtGui.QIcon('icon.ico'))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #self.ui.im.setPixmap(QPixmap(QImage.fromData(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACmElEQVRYR8VXTW7TUBD+xjYSXZFukOIsSE9AskNJJMoJmq4r7OYEwAkabhBOkB/Emt4gVIojdpgbpIumEitX6gKB7UHPkauXxLHfc4F6Z3l+vvnmm/fGhAd+6IHzQwvA9cfOITMfAdQAcx1EdVEAM/tEFADsWyaPn57MfdXClABcT1qnzHSWJiwMzrwgoF91vXGRbS6AH59ajd8hDYmoURQo67tgxoij42rv62KX/04Agu44xmciVMokT32YERgGjquvZ1+y4mQCWPUa0/sk3vQlwqssEFsAVrQbU4XKL/ai2+5PPK6waQ4AOsoDnDARh83NdmwBuJq0fQI9L6p+L7rd3+/5gbAToMPI+FbkIzRRc72mbLcGIFE7jGFRIPHddmZrvstJh1X8CHGv6sxHqe1GkPYCoGcqgcoCAPPCdr2DLQC6wqMoPEj7qdqCNKllxs30sLpjYDluDUDGG5XqhY2sal3w4PiD7c7fJnHShMtJR8zpy/8CALiwndnhBgD1/t+XAXkaZAaUVHwnHulg0W6BNEWlAQD8zna8gQB0Ne70iXCm2j55jCUAei1gxvuaO+uXAcDg7zXHSy640iKUAehOEDJFqDmGQkiPLO5Fv+KADXOqvCuIsrPGsIyQdHou22YeRMJgOdHTQTkAfGk7XrLKrWlAvOhcRgBfWiZ3RQti0zxXuUFXCXMuo0TRitfxugjbIxC5RYzI6s9kIGFh+KLOpiW22id5AUuI8IaisFG4kCQg/sFKJgtPLix3KWXGeRETRbQDuCFCV2spTYMm+2FEI1WBbYIRPTeiqFtqLZeDraaD+qrbkpgQAvfl1WsXU0p/RjIjYYhTkNFgcCVlRlRKoAAc+5aF0V//NVPoc2kTLQZKZ8lx/AMXBmMwuXUwOAAAAABJRU5ErkJggg=='))))
        #qApp.setStyleSheet("QMessageBox QPushButton{background-color: white;}")
        #self.ui.text.setText(random.choice(cita.croyons))
        self.ui.text.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        MainWindow.setGeometry(self,5, int(height/1.5), 507, 307)
        MainWindow.setWindowFlags(self,
                             QtCore.Qt.WindowStaysOnTopHint
                             | QtCore.Qt.FramelessWindowHint
                             | QtCore.Qt.Tool)
        MainWindow.setAttribute(self,QtCore.Qt.WA_TranslucentBackground)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.citation =""
        self.auteur="rami"
        self.init()
        self.afficheNotif()
        self.ui.valider.clicked.connect(lambda : self.enregistrer())
        self.ui.edit.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.annuler.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.hparleur.clicked.connect(lambda : threading.Thread(target=lambda : self.speak()).start())
        self.ui.actualiser.clicked.connect(lambda : self.afficheNotif())
        self.ui.copy.clicked.connect(lambda : self.copy())

        self.ui.close.clicked.connect(lambda : ui.close())
        #utilisation de threading pour recevoir un signal(le message apres le temps ecoule) provenant de la class syncWorker
        self.worker = syncWorker()
        self.workerThread = QThread() #deplace le Worker object au Thread object
        self.workerThread.started.connect(self.worker.loop) #init worker loop
        self.worker.moveToThread(self.workerThread)
        self.worker.setMess.connect(self.afficheNotif)
        self.workerThread.start()


    def init(self):
        if os.path.isfile("citations.txt") : pass
        else:
            self.add_cita_default()
            
        self.auteur_defaut ="rami"
    #fonction qui affiche le message

    def add_cita_default(self):
        cita = """{'malika': 'se tromper est humain, persister dans son erreur est diabolique, voilà pourquoi je me repends',
'martin': "j'ai cru bien fait, aujourd8 je m'en rends compte de mon immense erreur",'malika': "je suis vraiment desolé pour tout sa",'malika': "ma tendre amie, que je regrette tant, j'aimerais encore être ton amie",
'martin': "je tiens à notre amitié bien plus que tu ne l'imagine",'malika': "j'essaie d'aprendre de chaque erreur, helas c'est encore insuffisant",
'martin': "je suis sincerement desolé rami",'malika': "le coeur saignant je demande au bon Dieu de m'excuser pour tes ses manquements, à toi aussi ...",'martin': "jamais je pourrais te promettre d'être une bonne personne mais te dire que chaque fois que je serais à terre j'essaierais de me relever",'malika': "quoi qu'il m'en coute je serais spetacteur de ta vie toute ma vie, proche ou pas",'malika': "que des regrets pour l'amie, un coeur saignant pour un coeur aimant",'malika': "je passerais mon temps à ecrire pour m'excuser mais c'est encore insuffisant",'malika': "le bon Dieu s'occupe si bien de toi que ma pauvre amitié ne saurait apporté mais j'ose croire qu'Il se servira de moi même qu'une seul fois pour t'apporter un leger sourit",'malika': "mes regrets se levent tout comme le soleil et me ronge jusqu'a la nuit, tes ecris comme une lune adouci mon coeur",'malika': "je me souviendrais mais je ferais bien plus , je m'excuserais tant que je pourrait par tous les moyens que je trouverais",'malika': "Que des erreurs, Que je te comprends, Jamais je t'en voudrais j'espere juste qu'un jour tu me comprendras et tu m'excusera",'malika': "haras mira, souviens toi de fixer le bon Dieu toute ta vie, voilà l'essentiel!",'malika': "je t'ai jamais trailli, je me suis absenté voilà pourquoi je m'en veux, n'empeche que je te serais toujours fidèle",'malika': "Juste ton bonheur et rien d'autre, j'ai jamais rien espéré d'autre, prends bien soin de toi !",'malika': "j'ai pas su être un ami à la hauteur, vraiment desolé ....",'malika': "j'ai beaucoup appris et je continuerais d'apprendre de toi, daigne m'excuser ..."}"""
        
        with open("citations.txt","w") as f: f.write(cita)
    def afficheNotif(self):
        if int(random.random()*4)&2==0 :
            ft=tempfile.mkstemp(suffix = '.html')[-1]
            with open(ft) as f :
                f.write("""<html> <div class="box"><i class="fas fa-quote-left fa2"></i>
                  <div class="text"><i class="fas fa-quote-right fa1"></i>
                    <div>
                      <h3>Souviens Toi </h3>
                      <p>
                souviens toi que tu es le fruit de l'Amour de Dieu <br>
                souviens toi que tes choix doivent faire place au choix du Christ <br>
                <!--souviens toi de tes plus beau ecris, je prendrais plaisir à les conserver <br>-->
                pour ma part j'ai que des excuses tout pourrit <br>
                pour ma part j'aurais toujours de l'espoir d'être de nvo ton ami<br>
                pour ma part je suis desolé ... <br>
                haras Mira !.</p>
                    </div>
                  </div>
                </div>

                <style>
                * {
                  -webkit-box-sizing: border-box;
                  -moz-box-sizing: border-box;
                  box-sizing: border-box;
                  padding: 0;
                  margin: 0;
                }

                body {
                  background-color: #b71540;
                  font-family: "Montserrat", sans-serif;
                }

                .box {
                  background-color: transparent;
                  border-radius: 3px;
                  color: #fff;
                  position: absolute;
                  top: 50%;
                  left: 50%;
                  transform: translate(-50%, -50%);
                  width: 400px;
                  height: 300px;
                  transform-style: preserve-3d;
                  perspective: 2000px;
                  transition: 0.4s;
                  text-align: center;
                }
                .box:before {
                  content: "";
                  position: absolute;
                  top: 0;
                  left: 0;
                  width: 100%;
                  height: 100%;
                  background: transparent;
                  border-top: 20px solid #fff;
                  border-left: 20px solid #fff;
                  box-sizing: border-box;
                }
                .box:after {
                  content: "";
                  position: absolute;
                  top: 0;
                  left: 0;
                  width: 100%;
                  height: 100%;
                  border-bottom: 20px solid #fff;
                  border-right: 20px solid #fff;
                  box-sizing: border-box;
                }.box .fas {
                  font-size: 25px;
                  height: 50px;
                  width: 50px;
                  line-height: 50px !important;
                  background-color: #fff;
                  color: #2C3A47;
                }
                .box .fa2 {
                  position: absolute;
                  bottom: 0;
                  right: 0;
                  z-index: 1;
                }
                .box .text {
                  position: absolute;
                  top: 30px;
                  left: -30px;
                  width: calc(100% + 60px);
                  height: calc(100% - 60px);
                  background-color: #2C3A47;
                  border-radius: 3px;
                  transition: 0.4s;
                }
                .box .text .fa1 {
                  position: absolute;
                  top: 0;
                  left: 0;
                }
                .box .text div {
                  position: absolute;
                  top: 50%;
                  left: 0;
                  transform: translateY(-50%);
                  text-align: center;
                  width: 100%;
                  padding: 30px 60px;
                  line-height: 1.5;
                  box-sizing: border-box;
                }
                .box .text div h3 {
                  font-size: 30px;
                  margin-bottom: 5px;
                }
                .box .text div p {
                  font-size: 15px;
                }
                .box:hover {
                  transform: translate(-50%, -50%) rotateY(-20deg) skewY(3deg);
                }
                .box:hover .text {
                  transform: rotateY(20deg) skewY(-3deg);
                }
                </style>
                </html>""")
            webbrowser.open(ft)
        #if self.isVisible
        self.loadCita()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.text.setText(self.citation)
        self.ui.auteur.setText("- "+self.auteur)
        self.show()
        
    def loadCita(self):
        try:
            with open("citations.txt","r") as f:
                citations = eval(f.read())
                self.auteur,self.citation = random.choice(list(citations.items()))
                if len(self.auteur)<2 : self.auteur = self.auteur_defaut
        except Exception as e:
            print("erreur de lecture")
            print(e)
            
            self.citation="erreur d'affichage, navré !"

    def enregistrer(self):
        try:
            with open("citations.txt","r") as f:citations = eval(f.read())
            text= self.ui.text_cita.toPlainText()
            auteur = self.ui.auteur_cita.text()
            if len(text)>5 :
                if len(auteur)<2 : auteur = "rami"
                citations[auteur]=text
                with open("citations.txt","w") as f:
                        f.write(str(citations))
                QMessageBox.information(self, "copie ok",  """<font color='white'><p><b>Citation bien enregistré</b></p>""")
                self.ui.text_cita.setText("")
                self.ui.auteur_cita.setText("")
            else:
                QMessageBox.information(self, "copie ok",  """<font color='white'><p><b>renseigne bien les champs!</b></p>""")
        except Exception as e:
            print("erreur d'ecriture")
            print(e)

    def speak(self):
        #time.sleep(2)
  
        engine = pyttsx3.init()
        if engine._inLoop:
            engine.endLoop()
        engine = pyttsx3.init()
        engine.setProperty("rate",150)
        engine.say(self.citation) 
        # engine.say(text1) 
        # engine.say(text2) 
        # engine.say(text3) 
        engine.runAndWait()

    def copy(self):
        pyperclip.copy(self.citation)
        spam = pyperclip.paste()
        QMessageBox.information(self, "copie ok",  """<font color='white'><p><b>Text bien copié</b></p>""")
        
        """msg = QMessageBox()
        msg.setText("Text bien copié")
        msg.setWindowTitle("copie")
        #msg.setWindowIcon(QtGui.QIcon("black tic.png"))
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("background-color: rgb(255,255, 250);")
        msg.setStyleSheet("text-color: rgb(0, 0, 0);")
        msg.show()"""
    def closeEvent(self,event):
        self.hide()

    def mousePressEvent(self, event):
        
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.ico'))
    screen_rect = app.desktop().screenGeometry()
    width, height = screen_rect.width(), screen_rect.height()
    #time.sleep(3)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
