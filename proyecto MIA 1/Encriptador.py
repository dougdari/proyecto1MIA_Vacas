import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

def encriptar(data):
    data = pad(data.encode(),16)
    cipher = AES.new('miaproyecto12345'.encode('utf-8'), AES.MODE_ECB)
    return binascii.hexlify(cipher.encrypt(data))

def desencriptar(data):
    data = binascii.unhexlify(data)
    cipher = AES.new('miaproyecto12345'.encode('utf-8'),AES.MODE_ECB)
    return unpad(cipher.decrypt(data),16)


encriptado = encriptar('junio1234')
print('Encriptado: ',encriptado.decode("utf-8","ignore"))

desencriptado = desencriptar(encriptado)
print("Desencriptado: ",desencriptado.decode("utf-8","ignore"))