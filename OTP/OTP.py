import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import customtkinter
import random
import time

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.geometry("500x400")

# Global değişkenler
kalan_giriş_sayısı = 3
son_giris_zamani = 0
otp_sifre = None
alici_email = ""


def update_countdown():
    remaining_time = int(countdown_end_time - time.time())
    if remaining_time >= 0 and kalan_giriş_sayısı != 5 and kalan_giriş_sayısı >= 0:  # Eğer süre bitmediyse ve giriş hakkı varsa
        countdown_label.configure(text=f"Kalan Süre: {remaining_time} saniye")
        countdown_label.after(1000, update_countdown)  # Her 1 saniyede bir güncelle
    else:
        countdown_label.configure(text="")
def start_countdown():
    global countdown_label
    global countdown_end_time

    countdown_end_time = time.time() + 60 #60 saniye

    update_countdown()

def kalan_girişi_kontrol():
    global kalan_giriş_sayısı
    kalan_giriş_sayısı = 3

def otp():
    kalanhakk_label.configure(text=f"")
    kalan_girişi_kontrol()
    start_countdown()
    global otp_sifre
    global son_giris_zamani
    global alici_email

    alici_email = entry1.get()  # Kullanıcının girdiği e-posta adresi
    son_giris_zamani = time.time()

    gonderici_email = "bbayir686@gmail.com"
    gonderici_sifre = "sdhd hrlf lfvg frfi"
    otp_sifre = random.randint(100000, 999999)

    baslik = "Konu: Tek Kullanımlık Şifre (OTP) Doğrulaması"
    icerik = f"""Merhaba,

    Tek Kullanımlık Şifreniz (OTP) aşağıdaki gibidir. Bu şifre, 1 dakika içinde geçersiz hale gelecektir:

    OTP Şifresi: {otp_sifre}

    Geri bildiriminiz için teşekkür ederiz.

    """

    msg = MIMEMultipart()
    msg['From'] = gonderici_email
    msg['To'] = alici_email
    msg['Subject'] = baslik

    msg.attach(MIMEText(icerik, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gonderici_email, gonderici_sifre)
        server.sendmail(gonderici_email, alici_email, msg.as_string())
        server.quit()
        print("E-posta başarıyla gönderildi.")
    except Exception as e:
        print(f"Hata oluştu: {e}")

def analiz():
    global kalan_giriş_sayısı
    global otp_sifre
    global son_giris_zamani

    giris_otp = entry2.get()  # Kullanıcının girdiği OTP

    if time.time() - son_giris_zamani > 60:
        print("Süre doldu, lütfen yeni bir OTP isteyin.")
        return

    if int(giris_otp) == otp_sifre:
        print("Giriş başarılı.")
        kalan_giriş_sayısı = 5
        kalanhakk_label.configure(text=f"giriş başarılı")
        countdown_label.configure(text=f"")

    else:
        kalan_giriş_sayısı -= 1
        if kalan_giriş_sayısı >= 0:
            print(f"${kalan_giriş_sayısı} kadar hakkınız kaldı, lütfen tekrar deneyin.")
            kalanhakk_label.configure(text=f"Kalan Hak Sayısı: {kalan_giriş_sayısı}")
        else :
            print(f"giriş hakkınız bitti, lütfen tekrar otp isteyiniz.")
            kalanhakk_label.configure(text=f"tekrar OTP isteyiniz")
         # Yanlış giriş sayısını sıfırla

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20,padx=60,fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Anlık Şifre Sistemi")
label.pack(pady=20, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="mail")
entry1.pack(pady=12, padx=10)

button1 = customtkinter.CTkButton(master=frame, text="şifreyi gönder", command=otp)
button1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="şifre")
entry2.pack(pady=12, padx=10)

button2 = customtkinter.CTkButton(master=frame, text="şifreyi doğrula", command=analiz)
button2.pack(pady=12, padx=10)

kalanhakk_label = customtkinter.CTkLabel(master=frame, text="", font=("Arial", 12))
kalanhakk_label.pack(side="top", anchor="sw", pady=10, padx=140)

countdown_label = customtkinter.CTkLabel(master=frame, text="", font=("Arial", 12))
countdown_label.pack(side="bottom", anchor="se", pady=10, padx=10)

root.mainloop()