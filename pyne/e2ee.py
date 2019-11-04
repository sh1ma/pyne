import os
import collections

import urllib.parse
import base64
import hashlib
import Crypto.Cipher.AES as AES
# import axolotl_curve25519 as curve
from nacl.public import PrivateKey, Box

E2EEKeyPair = collections.namedtuple("E2EEKeyPair", ["private_key", "public_key"])
AESKeyAndIv = collections.namedtuple("AESKeyAndIv", ["Key", "iv"])

KEY = "Key".encode("utf-8")
IV = "IV".encode("utf-8")


def generate_asymmetric_keypair():
    # private_key = curve.generatePrivateKey(os.urandom(32))
    # public_key = curve.generatePublicKey(private_key)
    private_key = PrivateKey(private_key=os.urandom(32))
    public_key = private_key.public_key


    return E2EEKeyPair(private_key, public_key)


def generate_query(public_key) -> str:
    secret = urllib.parse.quote(base64.b64encode(public_key).decode("utf-8"))

    return f"secret={secret}&e2eeVersion=1"


def generate_shared_secret(private_key, public_key):
    # shared_secret = curve.calculateAgreement(private_key, public_key)
    shared_secret = Box(private_key, public_key).shared_key()

    return shared_secret


def half_xor_data(buf):
    buf_length = len(buf)
    if buf_length % 2 != 0:
        raise Exception("error")
    buf2 = bytearray(int(buf_length/2))
    for i in range(int(buf_length/2)):
        buf2[i] = buf[i] ^ buf[len(buf2) + i]
    return bytes(buf2)

def sha256(buf):
    return hashlib.sha256(buf).digest()


def generate_aes_key_and_iv(shared_secret):
    aes_key = sha256(shared_secret + KEY)
    aes_iv = half_xor_data(sha256(shared_secret + IV))
    # print(len(aes_iv))

    return AESKeyAndIv(aes_key, aes_iv)


def generate_signature(aes_key, encrypted_data):
    data = half_xor_data(sha256(encrypted_data))
    signature = encrypt_data_with_aes_ecb(aes_key, data)

    return signature


def verify_signature(signature, aes_key, encrypted_data):
    data = half_xor_data(sha256(encrypted_data))

    return bool(decrypt_data_with_aes_ecb(aes_key, signature) == data)


def encrypt_data_with_aes(aes_key, aes_iv, plain_data):
    aes = AES.new(aes_key, AES.MODE_CBC, aes_iv)

    return aes.encrypt(plain_data)


def encrypt_data_with_aes_ecb(aes_key, plain_data):
    aes = AES.new(aes_key, AES.MODE_ECB)

    return aes.encrypt(plain_data)


def decrypt_data_with_aes(aes_key: bytes, aes_iv: bytes, encrypted_data: bytes):
    aes = AES.new(aes_key, AES.MODE_CBC, aes_iv)

    return aes.decrypt(encrypted_data)


def decrypt_data_with_aes_ecb(aes_key, encrypted_data):
    aes = AES.new(aes_key, AES.MODE_ECB)

    return aes.decrypt(encrypted_data)

def decrypt_keychain(keypair, encrypted_keychain, public_key):
    private_key = keypair.private_key
    public_key = base64.b64decode(public_key)
    encrypted_keychain = base64.b64decode(encrypted_keychain)
    shared_secret = generate_shared_secret(private_key, public_key)
    # a = half_xor_data(sha256(encrypted_keychain))
    aes_key, aes_iv = generate_aes_key_and_iv(shared_secret)
    keychain_data = decrypt_data_with_aes(aes_key, aes_iv, encrypted_keychain)

    return keychain_data
