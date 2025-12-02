import random
from typing import Tuple, List
from Crypto.Util import number  # быстрый генератор простых чисел

# -----------------------------
# ElGamal
# -----------------------------

def generate_keys(bits=32):
    """
    Генерация ключей ElGamal с использованием PyCryptodome.
    Возвращает public_key (dict) и private_key (int)
    """
    p = number.getPrime(bits)  # быстрое простое число
    g = find_primitive_root_fast(p)  # быстрый первообразный корень

    x = random.randrange(2, p - 1)  # приватный ключ
    y = pow(g, x, p)                # публичный ключ

    public_key = {"p": p, "g": g, "y": y}
    private_key = x

    return public_key, private_key


def find_primitive_root_fast(p: int) -> int:
    """
    Быстрый поиск первообразного корня для учебного проекта.
    Для больших чисел случайный перебор и fallback на 2.
    """
    if p == 2:
        return 1

    phi = p - 1
    factors = set()
    n = phi
    i = 2
    while i * i <= n:
        if n % i == 0:
            factors.add(i)
            while n % i == 0:
                n //= i
        i += 1
    if n > 1:
        factors.add(n)

    for _ in range(1000):  # пробуем 1000 случайных g
        g = random.randrange(2, p)
        if all(pow(g, phi // f, p) != 1 for f in factors):
            return g

    return 2  # fallback


def encrypt_message(message: bytes, public_key) -> List[Tuple[str, str]]:
    """
    Шифрование сообщения кусками.
    Возвращает список кортежей (c1, c2) как строки
    """
    p = public_key["p"]
    g = public_key["g"]
    y = public_key["y"]

    chunk_size = (p.bit_length() // 8) - 1
    chunks = [message[i:i + chunk_size] for i in range(0, len(message), chunk_size)]

    encrypted_chunks = []

    for chunk in chunks:
        m = int.from_bytes(chunk, "big")
        k = random.randrange(2, p - 1)

        c1 = pow(g, k, p)
        s = pow(y, k, p)
        c2 = (m * s) % p

        encrypted_chunks.append((str(c1), str(c2)))

    return encrypted_chunks


def decrypt_message(encrypted_chunks, public_key, private_key) -> bytes:
    """
    Расшифровка сообщения.
    encrypted_chunks — список кортежей (c1, c2)
    Возвращает исходные байты
    """
    p = public_key["p"]
    x = private_key

    decrypted = []

    for c1_str, c2_str in encrypted_chunks:
        c1 = int(c1_str)
        c2 = int(c2_str)

        s = pow(c1, x, p)
        s_inv = pow(s, -1, p)
        m = (c2 * s_inv) % p

        chunk = m.to_bytes((m.bit_length() + 7) // 8, "big")
        decrypted.append(chunk)

    return b"".join(decrypted)