import string


def encrypt_atbash(plaintext: str) -> str:
    ciphertext = ""
    upper_alphabet = string.ascii_uppercase
    lower_alphabet = string.ascii_lowercase

    encrypted_upper = upper_alphabet[::-1]
    encrypted_lower = lower_alphabet[::-1]

    encryption_table = str.maketrans(upper_alphabet + lower_alphabet, encrypted_upper + encrypted_lower)
    ciphertext = plaintext.translate(encryption_table)
    return ciphertext


if __name__ == "__main__":
    example = "Hello, World!55"
    encrypted = encrypt_atbash(example)
    print(f"Was given: {example}")
    print(f"Was encrypted: {encrypted}")
