import gmpy2
from gmpy2 import mpz

N = mpz("64806601923671")
e = 3676721
C = mpz("20691828453967585515826195335268721092016820981648665029191116174852454100651527277132921218603675639270359132114438767538210428120181826834881231944035515451410453551")

def fermat_factorization(n):
    a = gmpy2.isqrt(n) + 1
    b2 = a * a - n
    while not is_perfect_square(b2):
        a += 1
        b2 = a * a - n
    b = gmpy2.isqrt(b2)
    p = a - b
    q = a + b
    return p, q

def is_perfect_square(x):
    return x >= 0 and gmpy2.isqrt(x) ** 2 == x

def decrypt(C, d, N):
    return pow(C, d, N)

p, q = fermat_factorization(N)

phi_N = (p - 1) * (q - 1)

d = gmpy2.invert(e, phi_N)



decrypted_message = decrypt(C, d, N)
num_bytes = (decrypted_message.bit_length() + 7) // 8
decrypted_bytes = decrypted_message.to_bytes(num_bytes, byteorder='big')
decrypted_string = decrypted_bytes.decode('utf-8', errors='ignore')
decrypted_message_bytes = int(decrypted_message).to_bytes((decrypted_message.bit_length() + 7) // 8, 'big')
numeric_representation = [str(byte) for byte in decrypted_message_bytes]

print(f"Множители: p = {p}, q = {q}")
print(f"Функция Эйлера φ(N) = {phi_N}")
print(f"Обратное значение экспоненты d = {d}")
print("Дешифрованный текст (в числовом виде):", ' '.join(numeric_representation))
