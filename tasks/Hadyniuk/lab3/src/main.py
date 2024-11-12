import math
from sympy import mod_inverse

# Данные
N = 95841214023781
e = 2005229
cipher_blocks = [
    49190327214217,
    84609592142386,
    90112415897890,
    58321768145112,
    18048020096041,
    46703140105758,
    5914356051570,
    1805696039350,
    28838003818624,
    70062757763886,
    13846553049563,
    90432970156505
]

# Функция для факторизации N (может занять много времени)
def factorize_n(N):
    for i in range(2, int(math.sqrt(N)) + 1):
        if N % i == 0:
            return i, N // i
    return None

# Факторизация N
p, q = factorize_n(N)
if p and q:
    print(f"p = {p}, q = {q}")
    
    # Вычисление φ(N)
    phi_n = (p - 1) * (q - 1)

    # Вычисление закрытого ключа d
    d = mod_inverse(e, phi_n)
    print(f"Закрытый ключ d = {d}")

    # Функция для расшифровки блока
    def decrypt_block(c, d, N):
        return pow(c, d, N)

    # Расшифровка всех блоков
    decrypted_blocks = [decrypt_block(c, d, N) for c in cipher_blocks]

    # Преобразование блоков в hex-строку и декодирование в windows-1251
    decoded_message = ""
    for block in decrypted_blocks:
        # Преобразуем расшифрованное число в hex
        hex_block = hex(block)[2:]  # Убираем префикс "0x"
        
        # Если длина hex нечетная, добавляем 0 в начале
        if len(hex_block) % 2 != 0:
            hex_block = '0' + hex_block
        
        try:
            # Преобразуем hex в байты
            bytes_block = bytes.fromhex(hex_block)
            
            # Декодируем байты в строку с использованием windows-1251
            decoded_message += bytes_block.decode('windows-1251')
        except UnicodeDecodeError:
            print(f"Ошибка декодирования блока: {hex_block}")

    # Вывод расшифрованного сообщения
    print("Расшифрованное сообщение:")
    print(decoded_message)
else:
    print("Не удалось факторизовать N")
