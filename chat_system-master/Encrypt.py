
import sys
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
 
class encryptor():
    def __init__(self, key):
        self.key = key 
        self.mode = AES.MODE_CBC

    
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        #Length of the key here must be 16（AES-128）、24（AES-192）、or 32（AES-256）Bytes
        length = 16
        count = len(text)
        #If the length of text cannot be devided by 16，fill the vacancy
        add = length - (count % length)
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        #As the result might not be a part of the ASCII, and a problem
        #might occur if we send it to the terminal, we transform it into a hexstring
        #And as json needs string, we decode it
        return b2a_hex(self.ciphertext).decode()

     
    
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)

        plain_text = cryptor.decrypt(a2b_hex(text)).decode()
        return plain_text.rstrip('\0')
        #After decryption, delete all the zeroes we used to fill the vacancy
 

