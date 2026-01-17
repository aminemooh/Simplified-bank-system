class VigenereCipher:
    """Encrypt and decrypt text using the Vigenère cipher.
    The key must be a non-empty string of alphabetic characters.
    Non-alphabetic characters in the input are preserved unchanged,
    and the case of letters is preserved.
    """
    def __init__(self, key):
           # Initialize the cipher with a given key.
        if not key:
            raise ValueError("Key must be a non-empty string of letters.")
        if not key.isalpha():
            raise ValueError("Key must contain letters only (A-Z or a-z).")
           # Store a normalized uppercase version for internal use.
        self._key = key.upper()
           # Precompute numeric shifts (0–25) for each key character.
        self._shifts = [self._char_to_shift(c) for c in self._key]

    @staticmethod
    def _char_to_shift(ch):
        #Convert a key character (A–Z or a–z) to a shift in the range 0–25.
        return ord(ch.upper()) - ord("A")

    @staticmethod
    def _shift_char(ch, shift, encrypt=True):
        #Shift a single alphabetic character by `shift` positions.
        if ch.isupper():
            base = ord("A")
        else:
            base = ord("a")
        offset = ord(ch) - base
        if encrypt:
            new_offset = (offset + shift) % 26
        else:
            new_offset = (offset - shift) % 26
        return chr(base + new_offset)

    def _process(self, text, encrypt):
           #Core transformation used by both encrypt and decrypt.
        if not text:
            return ""
        result_chars = []
        key_index = 0
        key_length = len(self._shifts)
        for ch in text:
            if ch.isalpha():
                shift = self._shifts[key_index % key_length]
                key_index += 1
                result_chars.append(self._shift_char(ch, shift, encrypt=encrypt))
            else:
                result_chars.append(ch)
        return "".join(result_chars)

    def encrypt(self, plaintext):
           #Encrypt plaintext using the Vigenère cipher.
        return self._process(plaintext, encrypt=True)

    def decrypt(self, ciphertext):
           #Decrypt ciphertext using the Vigenère cipher.
        return self._process(ciphertext, encrypt=False)
