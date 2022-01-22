from selenium import webdriver
import time
import sys
from PyQt5 import QtWidgets


class Pencere(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):  
        self.setGeometry(500,250,350,300)
        self.setWindowTitle("İnstagram Beğeni Botu")
        v_box = QtWidgets.QVBoxLayout()

        self.label1 = QtWidgets.QLabel("Kullanıcı Adı")
        self.username = QtWidgets.QLineEdit()
        self.label2 = QtWidgets.QLabel("Parola")
        self.password = QtWidgets.QLineEdit()
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.label3 = QtWidgets.QLabel("Etiketler: Her etiket başına # işareti koymayı ve virgülle ayırmayı unutmayın")
        self.etiketler = QtWidgets.QLineEdit()
        self.label4 = QtWidgets.QLabel("Beğeni Sayısı")
        self.begeni = QtWidgets.QLineEdit()
        self.buton = QtWidgets.QPushButton("Başla")

        v_box.addWidget(self.label1)
        v_box.addWidget(self.username)
        v_box.addWidget(self.label2)
        v_box.addWidget(self.password)
        v_box.addWidget(self.label3)
        v_box.addWidget(self.etiketler)
        v_box.addWidget(self.label4)
        v_box.addWidget(self.begeni)
        v_box.addWidget(self.buton)
        v_box.addStretch()

        self.setLayout(v_box)
        self.buton.clicked.connect(self.click)
        self.show()


    def click(self):

        liste = self.etiketler.text().split(",")
        # instagrama git
        brow = webdriver.Firefox()
        url = "https://www.instagram.com/"
        brow.get(url)
        time.sleep(4)

        # giriş yap
        usernam = brow.find_element_by_css_selector("[name='username']")
        passwor = brow.find_element_by_css_selector("[name='password']")
        usernam.send_keys(self.username.text())
        passwor.send_keys(self.password.text())
        login_button = brow.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div")
        login_button.click()

        # şimdi değil
        time.sleep(10)
        not_now = brow.find_element_by_css_selector("[class='cmbtv']")
        not_now.click()
        time.sleep(4)
        not_now2 = brow.find_element_by_css_selector("[class='aOOlW   HoLwm ']")
        not_now2.click()
        time.sleep(5)

        # etiket gönder postları bul
        find = brow.find_element_by_css_selector("[placeholder='Search']")
        find.send_keys(liste[0])
        time.sleep(2)
        fidn_button =  brow.find_element_by_css_selector("[class='_7UhW9   xLCgt       qyrsm KV-D4          uL8Hv         ']")
        fidn_button.click()
        time.sleep(8)
        post = brow.find_element_by_css_selector("[class='v1Nh3 kIKUG  _bz0w']")
        post.click()
        time.sleep(7)

        # ilk etiketin postlarını beğen
        a= 0
        next_button = brow.find_element_by_css_selector("[class=' _65Bje    coreSpriteRightPaginationArrow']")
        def goto(linenum):
            global line
            line = linenum

        while a < int(self.begeni.text()):
            try:   
                time.sleep(1)
                like = brow.find_element_by_css_selector("[aria-label='Like'][width='24']")            
                like.click()
                a += 1                
                next_button.click()
                time.sleep(2)
            except:
                print("Beğenilmiş")
                next_button.click()
                goto(79)
            
        #postu kapat
        time.sleep(2)
        close = brow.find_element_by_css_selector("[aria-label='Close']")
        close.click()
        time.sleep(1)

        # başka etikete geç
        liste.pop(0)
        for i in liste:
            # etiket gönder
            find = brow.find_element_by_css_selector("[placeholder='Search']")
            find.send_keys(i)
            time.sleep(2)
            fidn_button =  brow.find_element_by_css_selector("[class='_7UhW9   xLCgt       qyrsm KV-D4          uL8Hv         ']")
            fidn_button.click()
            time.sleep(7)
            post = brow.find_element_by_css_selector("[class='v1Nh3 kIKUG  _bz0w']")
            post.click()
            time.sleep(5)
            # Beğen
            a= 0
            while a < int(self.begeni.text()):
                try:   
                    time.sleep(1)
                    like = brow.find_element_by_css_selector("[aria-label='Like'][width='24']")            
                    like.click()
                    a += 1        
                    next_button = brow.find_element_by_css_selector("[class=' _65Bje    coreSpriteRightPaginationArrow']")        
                    next_button.click()
                    time.sleep(2)
                except:
                    print("Beğenilmiş")
                    next_button = brow.find_element_by_css_selector("[class=' _65Bje    coreSpriteRightPaginationArrow']")
                    next_button.click()
                    goto(113)
            #post kapat
            close = brow.find_element_by_css_selector("[aria-label='Close']")
            close.click()
            time.sleep(2)

        time.sleep(10)
        brow.close()
        time.sleep(5)
        print("İşlem Tamamlandı")
      
app = QtWidgets.QApplication(sys.argv)
pencere = Pencere()
sys.exit(app.exec_())