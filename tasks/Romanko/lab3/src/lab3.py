"""
N = 72903890242273
e = 3261683
C = [
37429454018574 
65632293727338 
71955235122455 
71474662312159 
18537435780920 
58372142077460 
68330829196451 
60882917270796 
24142764117328 
31238010810556 
66143215653810 
30769266886306 
]
"""
from sympy import factorint
from math import gcd

def euler_phi(n):
    count = 0
    for i in range(1, n + 1):
        if gcd(n, i) == 1:
            count += 1
    return count

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def number_to_text(number):
    message = ""
    while number > 0:
        message = chr(number % 256) + message
        number //= 256
    return message

def number_to_text_utf8(number):
    message = bytearray()
    while number > 0:
        message.insert(0, number % 256)
        number //= 256
    return message.decode('utf-8', errors='replace')

e = 3261683
C = 37429454018574
n = 72903890242273
factors = factorint(n)
print(f"Простые множители числа {n}: {factors}")

prime_one, prime_two = factors.keys()
print(f"Первый и второй простые множители: {prime_one}, {prime_two}")

phi_prime_one = euler_phi(prime_one)
print(f"Функция Эйлера для первого простого множителя: {phi_prime_one}")

phi_prime_two = euler_phi(prime_two)
print(f"Функция Эйлера для второго простого множителя: {phi_prime_two}")

nok = lcm(phi_prime_one, phi_prime_two)
print(f"НОК: {nok}")

d = pow(e, -1, nok)
print(f"Число обратное числу {e} по модулю {nok}: {d}")

M = pow(C, d, n)
decoded_message = number_to_text(M)
print(f"Расшифрованное сообщения {C} = {decoded_message}")