import subprocess
import re
import pandas as pd

# Wi-Fi profillerini ve şifrelerini almak için netsh komutunu çalıştır
profiles_data = subprocess.check_output('netsh wlan show profiles').decode('utf-8', errors="backslashreplace")
profiles = re.findall("All User Profile     : (.*)\r", profiles_data)

# SSID ve şifreleri saklamak için listeler
ssids = []
passwords = []

# Her profil için SSID ve şifreyi al ve listelere ekle
for profile in profiles:
    profile_info = subprocess.check_output(f'netsh wlan show profile "{profile}" key=clear').decode('utf-8',
                                                                                                    errors="backslashreplace")
    password = re.findall("Key Content            : (.*)\r", profile_info)

    ssids.append(profile)
    passwords.append(password[0] if password else None)

# DataFrame oluştur
wifi_df = pd.DataFrame({
    'SSID': ssids,
    'Password': passwords
})

# Excel dosyasına kaydet
wifi_df.to_excel("wifi_passwords.xlsx", index=False)

print("Wi-Fi şifreleri wifi_passwords.xlsx dosyasına kaydedildi.")
