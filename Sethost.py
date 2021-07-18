import os
import sys
from transliterate import translit
from subprocess import Popen, PIPE
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
    QTextEdit, QPushButton, QGridLayout,QVBoxLayout, QDesktopWidget, QMessageBox, QApplication)


CITY_MAP = {
    'красноярск': 'гу',
    'назарово': 'наз',
    'шарыпово': 'шар',
    'ачинск': 'ачин',
    'енисейск': 'енис',
    'лесосибирск': 'лесос',
    'туруханск': 'турух',
    'норильск':'норил',
    'северо-енисейск':'севен',
    'северо-енисейский':'севен',
    'шушенское':'шушен',
    'новосёлово':'новос',
    'новоселово':'новос',
    'дудинка':'дудин',
    'игарка':'игарк',
    'ванавара':'ванав',
    'краснотуранск':'кртур',
    'иланск':'илан',
    'идринское':'идрин',
    'казачинское':'казач',
    'казачинск':'казач',
    'ермаковское':'ермак',
    'дзержинское':'дзерж',
    'курагино':'кураг',
    'сухобузимское':'сухоб',
    'сухобузимо':'сухоб',
}


class ARMSetup(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    

    def on_click(self):

        #---User name handler---
        userNameValue = self.userName.text().lower()
        userNameTranslit = translit(userNameValue, language_code='ru', reversed=True)
        userNameTranslit = userNameTranslit.replace("'", "")

        #---User city handler---
        userCityValue = self.userCity.text().lower()
        if userCityValue in CITY_MAP:
            userCityValue = CITY_MAP[userCityValue]

        userCityTranslit = translit(userCityValue, language_code='ru', reversed=True)
        userCityTranslit = userCityTranslit.replace("'", "")
        
        #---User info handler---
        userInfoValue = self.userInfo.toPlainText().lower()

        #---Check names length---
        if len(userCityTranslit) > 5:
            userCityTranslit = userCityTranslit[:5]
        if len(userNameTranslit) > 7:
            userNameTranslit = userNameTranslit[:7]

        # Make host_name   
        host_name = 'sm-%s-%s' % (userCityTranslit, userNameTranslit)    
        if len(host_name) > 15:
            host_name = host_name[:15]
        
        # try:
        #     ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
        # except:
        #     ip = 'unknown'
        #     pass

        # sendMessage = "userCity=%s&userName=%s&userInfo=%s&hostname=%s&ip=%s" % (userCityValue, userNameValue, userInfoValue, host_name, ip)
        
        echoMessage = "Заданое имя компьютера:  %s\n\nКомпьютер будет перезагружен" % (host_name)
        QMessageBox.about(self, " ",  echoMessage)
        
        shell_script = os.getcwd() + '/' + 'setup.sh'
        command = '%s %s' % (shell_script, host_name)
        p = os.system('echo %s|sudo -S %s' % ('ivb', command))

        #---Make record to /etc/hostname file---
        #command = 'echo %s > /etc/hostname' % (host_name)
        #print(command)
        #p = os.system('echo %s|sudo -S %s' % ('ivb', command))

        #---Set hostname command---
        #command = 'hostname -b %s' % (host_name)
        #p = os.system('echo %s|sudo -S %s' % ('ivb', command))

        #---Make reboot command---
        #command = 'reboot'
        #p = os.system('echo %s|sudo -S %s' % ('ivb', command))
        
        #---Close window---
        self.close()


    def initUI(self):

        self.userNameTitle = QLabel('Фамилия')
        self.userCityTitle = QLabel('Населенный пункт')
        self.userInfoTitle = QLabel('Контактные данные\n(email, номер телефона)\n\n*** Не обязательно')

        self.userName = QLineEdit()
        self.userCity = QLineEdit()
        self.userInfo = QTextEdit()

        saveButton = QPushButton('Применить')
        saveButton.clicked.connect(self.on_click)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.userNameTitle, 1, 0)
        grid.addWidget(self.userName, 1, 1)

        grid.addWidget(self.userCityTitle, 2, 0)
        grid.addWidget(self.userCity, 2, 1)

        grid.addWidget(self.userInfoTitle, 3, 0)
        grid.addWidget(self.userInfo, 3, 1, 5, 1)

        vertLayout = QVBoxLayout()
        vertLayout.addLayout(grid)
        vertLayout.addWidget(saveButton)

        self.setLayout(vertLayout)
        self.center()
        self.setWindowTitle('Настроить имя компьютера')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ARMSetup()
    sys.exit(app.exec_())
