import itertools

# Kriterlerin alınması
kelime_uzunlugu = int(input("Kelimenin uzunluğunu girin: "))
karakterler = input("Karakterler, rakamlar veya özel karakterler: ")
tekrar_sayisi = int(input("Harf/rakam/özel karakter tekrar etme sayısı: "))

# Kontroller
if tekrar_sayisi > kelime_uzunlugu:
    print("Hata: Tekrar sayısı, kelime uzunluğunu geçemez.")
    exit()

# Tüm kombinasyonların oluşturulması
tum_karakterler = list(karakterler)
kombinasyonlar = itertools.product(tum_karakterler, repeat=kelime_uzunlugu)
kelimeler = [''.join(comb) for comb in kombinasyonlar if max(comb.count(char) for char in comb) == tekrar_sayisi]

# Wordlist dosyasına yazılması
with open('wordlist.txt', 'w') as f:
    for kelime in kelimeler:
        f.write(f"{kelime}\n")

print(f"Wordlist 'wordlist.txt' dosyasına kaydedildi.")

def binary_search(wordlist, parola):
    sol = 0
    sag = len(wordlist) - 1

    while sol <= sag:
        orta = (sol + sag) // 2

        if wordlist[orta] == parola:
            return orta
        elif wordlist[orta] < parola:
            sol = orta + 1
        else:
            sag = orta - 1

    return -1

# Wordlist dosyasından verileri oku ve sıralı bir şekilde tut
with open('wordlist.txt', 'r') as f:
    wordlist = sorted([line.strip() for line in f])

# Kullanıcının girdiği parolayı al
parola = input("Aranacak parolayı girin: ")

# Parolanın uzunluğunu kontrol et
while len(parola) != kelime_uzunlugu:
    print(f"Parola uzunluğu {kelime_uzunlugu} olmalıdır. Lütfen tekrar girin.")
    parola = input("Aranacak parolayı girin: ")

# Binary search ile arama yap
sira = binary_search(wordlist, parola)

# Sonuçları göster
if sira != -1:
    print(f"Parola '{parola}' wordlist'te {sira+1}. sırada.")
else:
    print("Parola wordlist'te bulunamadı.")