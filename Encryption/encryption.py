import random
import string

chars = " " + string.punctuation + string.digits + string.ascii_letters # boşluk, noktalama işaretleri , rakamları ve ingilizce harfleri  atıyoruz
chars = list(chars) # bu diziyi bir liste haline getiriyoruz
key = chars.copy() # dizinin kopyasını key adlı diziye atıyoruz

random.shuffle(key) # key dizisini random bir şekilde karıştırıyoruz

#ENCRYPT
plain_text = input("Enter a message to encrypt: ") # kullanıcıdan aldığımız text
cipher_text = "" # şifrelenmiş text

for letter in plain_text:
    index = chars.index(letter)
    cipher_text += key[index]

print(f"original message : {plain_text}")
print(f"encrypted message: {cipher_text}")

#DECRYPT
cipher_text = input("Enter a message to encrypt: ")
plain_text = ""

for letter in cipher_text:
    index = key.index(letter)
    plain_text += chars[index]

print(f"encrypted message: {cipher_text}")
print(f"original message : {plain_text}")