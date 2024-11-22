def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# Функция для нахождения обратного по модулю
def mod_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Обратное по модулю не существует")
    return x % m


# Функция для нахождения целого корня n-й степени с проверкой
def integer_nth_root(x, n):
    high = 1
    while high ** n <= x:
        high *= 2
    low = high // 2
    while low < high:
        mid = (low + high) // 2
        if mid ** n < x:
            low = mid + 1
        else:
            high = mid
    return low - 1


def find_exact_root(S, e):
    # Находим приближённый корень
    M_approx = integer_nth_root(S, e)

    # Проверяем M_approx и M_approx + 1
    if (M_approx + 1) ** e <= S:
        return M_approx + 1
    else:
        return M_approx

russian_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def int_to_russian_text(val):
    result = []
    while val > 0:
        char_index = val % 100
        if 10 <= char_index <= 41:
            result.append(russian_alphabet[char_index - 10])
        else:
            print(f"Предупреждение: Недопустимое значение для символа: {char_index}. Пропускаем.")
            result.append(' ')
        val //= 100
    return ''.join(result[::-1])

def calcucalte(data):
    N1 = 363542076673
    N2 = 728740902979
    N3 = 522993716719
    C1 = data[0]
    C2 = data[1]
    C3 = data[2]
    e = 3

    # 1. Вычисляем произведения модулей
    M0 = N1 * N2 * N3
    m1 = N2 * N3
    m2 = N1 * N3
    m3 = N1 * N2

    # 2. Нахождение обратных по модулю для каждого случая
    n1 = mod_inverse(m1, N1)
    n2 = mod_inverse(m2, N2)
    n3 = mod_inverse(m3, N3)

    # 3. Применение китайской теоремы об остатках
    S = (C1 * n1 * m1 + C2 * n2 * m2 + C3 * n3 * m3) % M0
    M = find_exact_root(S % M0, e)
    print(M)


def main():
    with open("data.txt", "r") as file:
        data = [i[:-1] for i in file.readlines() if i != '']
        data = list(filter(None, data))
        data = list(map(int, data))
    data = list(zip(data[:12], data[12:24], data[24:]))
    for i in data:
        calcucalte(i)


if __name__ == "__main__":
    main()