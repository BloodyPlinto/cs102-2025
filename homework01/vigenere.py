import re

def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    keyword_upper = keyword.upper()
    shifts = [ord(k) - ord("A") for k in keyword_upper]
    key_length = len(keyword)
    russian_pattern = re.compile(r'[А-Яа-яЁё]')
    if russian_pattern.search(plaintext):
        raise ValueError("Only Latin letters are allowed in plaintext.")
    if russian_pattern.search(keyword):
        raise ValueError("Only Latin letters are allowed in keyword.")
    for i, char in enumerate(plaintext):
        if char.isalpha():
            shift = shifts[i % key_length]
            base = ord("A") if char.isupper() else ord("a")
            encrypted_char = chr((ord(char) - base + shift) % 26 + base)
            ciphertext += encrypted_char
        else:
            ciphertext += char
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    keyword_upper = keyword.upper()
    reverse_keyword = "".join(chr((26 - (ord(k) - ord("A"))) % 26 + ord("A")) for k in keyword_upper)
    plaintext = encrypt_vigenere(ciphertext, reverse_keyword)
    return plaintext
