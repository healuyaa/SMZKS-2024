import math

# Заданные значения
N = 84032429242009
e = 2581907
C = 54879925681459721670081829291782821975616617814399744948371366360800117722343426021542724152794267375927192643574021335775875169031132502017752005215695641247980943013

def fermat_factorization(N):
    """Факторизация числа N методом Ферма."""
    a = math.isqrt(N) + 1  # Начальное значение a
    b2 = a * a - N  # b^2 = a^2 - N

    while not is_perfect_square(b2):  # Пока b^2 не является полным квадратом
        a += 1
        b2 = a * a - N

    b = int(math.isqrt(b2))  # Получаем b
    p = a - b
    q = a + b
    return p, q

def is_perfect_square(x):
    """Проверка, является ли число x полным квадратом."""
    s = int(math.isqrt(x))
    return s * s == x

def extended_gcd(a, b):
    """Расширенный алгоритм Евклида для нахождения обратного по модулю."""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, phi):
    """Находит обратный элемент e по модулю phi."""
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise Exception('Обратный элемент не существует')
    else:
        return x % phi

def decrypt_rsa(N, e, C):
    """Расшифровка сообщения C."""
    p, q = fermat_factorization(N)  # Факторизация N
    phi = (p - 1) * (q - 1)  # Вычисление phi(N)
    d = mod_inverse(e, phi)  # Нахождение d

    # Расшифровка C
    M = pow(C, d, N)  # M = C^d mod N
    return M

# Основной блок
if __name__ == "__main__":
    # Расшифровка сообщения
    decrypted_message = decrypt_rsa(N, e, C)
    print("Дешифрованное сообщение (числовое):", decrypted_message)

    # Конвертация в строку (если сообщение закодировано в UTF-8 или ASCII)
    # Зависит от кодирования вашего сообщения
    try:
        #decrypted_text = bytearray.fromhex(hex(decrypted_message)[2:]).decode('utf-8')
        decrypted_text = bytearray.fromhex(hex(decrypted_message)[2:]).decode('latin-1')
        print("Дешифрованные байты:", bytearray.fromhex(hex(decrypted_message)[2:]))

        print("Дешифрованное сообщение (строка):", decrypted_text)
    except Exception as ex:
        print("Ошибка при конвертации в строку:", ex)

