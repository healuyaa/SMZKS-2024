from math import isqrt


def fermat_factorization(N):


    a = isqrt(N) + 1
    b2 = a * a - N


    while isqrt(b2) ** 2 != b2:
        a += 1
        b2 = a * a - N


    b = isqrt(b2)
    p = a - b
    q = a + b

    return p, q

def modinv(a, m):

    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Обратного элемента не существует")
    return x % m

def extended_gcd(a, b):

    if a == 0:
        return b, 0, 1
    g, y, x = extended_gcd(b % a, a)
    return g, x - (b // a) * y, y


def decrypt_rsa(C, d, N):

    return pow(C, d, N)




def rsa_fermat_attack(N, e, blocks):
    print(f"Факторизация N = {N} методом Ферма...")

    p, q = fermat_factorization(N)
    print(f"Факторы найдены: p = {p}, q = {q}")

    phi = (p - 1) * (q - 1)


    print(f"Вычисление закрытого ключа d...")
    d = modinv(e, phi)
    print(f"Закрытый ключ: d = {d}")


    decrypted_message = ""
    for C in blocks:
        print(f"Расшифровка блока: {C}")
        m = decrypt_rsa(C, d, N)
        print(f"Расшифрованное числовое сообщение: {m}")


        decrypted_message += str(m)+" "
    return decrypted_message


N = 99595193774911  
e = 1908299  
blocks = [
    75790643190143,
    36869061035180,
    38422576553598,
    68899435645717,
    16193161920958,
    98487458352335,
    34167725433806,
    96613844267045,
    26583768908805,
    73052827576371,
    94695336463618
] 


decrypted_message = rsa_fermat_attack(N, e, blocks)
print(f"Дешифрованное сообщение: {decrypted_message}")
