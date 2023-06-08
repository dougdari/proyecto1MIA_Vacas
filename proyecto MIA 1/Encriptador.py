import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

class AESencriptador:
    def __init__(self):
        pass

    def encriptar(self,data):
        data = pad(data.encode(),16)
        cipher = AES.new('miaproyecto12345'.encode('utf-8'), AES.MODE_ECB)
        return binascii.hexlify(cipher.encrypt(data))

    def desencriptar(self,data):
        data = binascii.unhexlify(data)
        cipher = AES.new('miaproyecto12345'.encode('utf-8'),AES.MODE_ECB)
        return unpad(cipher.decrypt(data),16)


#e = AESencriptador()
#encriptado = e.encriptar('junio1234')
#print('Encriptado: ',encriptado.decode("utf-8","ignore"))

#desencriptado = e.desencriptar(encriptado)
#print("Desencriptado: ",desencriptado.decode("utf-8","ignore"))