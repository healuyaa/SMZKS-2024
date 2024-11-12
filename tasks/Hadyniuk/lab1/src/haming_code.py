import math

def generate_hamming_code(M, r):
    # Перевод числа в двоичную систему счисления
    binary_M = bin(M)[2:]
    print(binary_M)
    # Определение количества информационных битов (M)
    M_bits = len(binary_M)

    # Полное количество битов в коде Хэмминга (M + r)
    n = M_bits

    # Инициализация кода Хэмминга с пустыми проверочными битами
    hamming_code = [0] * n

    # Вставка информационных битов на соответствующие позиции
    j = 0
    for i in range(n):
        if (i + 1) & i == 0:  # Пропуск позиций степеней двойки
            continue
        if j < M_bits:  # Проверка на выход за пределы
            hamming_code[i] = int(binary_M[j])
            j += 1

    # Функция для расчета значения проверочных битов
    def calculate_parity_bits(code, r):
        n = len(code)
        for i in range(r):
            parity_position = 2**i - 1
            if parity_position >= n:
                continue  # Если позиция проверочного бита выходит за границы кода
            parity = 0
            for j in range(parity_position, n, 2 * (parity_position + 1)):
                parity ^= sum(code[j:j + parity_position + 1])
            code[parity_position] = parity % 2
        return code

    # Рассчитываем значение проверочных битов
    hamming_code = calculate_parity_bits(hamming_code, r)
    return hamming_code

def introduce_error(hamming_code, position):
    # Инвертируем бит на указанной позиции (вводим ошибку)
    hamming_code[position] = 1 - hamming_code[position]
    return hamming_code

def detect_and_fix_error(hamming_code, r):
    n = len(hamming_code)
    error_position = 0

    # Вычисляем синдром для поиска позиции ошибки
    for i in range(r):
        parity_position = 2**i - 1
        parity = 0
        for j in range(parity_position, n, 2 * (parity_position + 1)):
            parity ^= sum(hamming_code[j:j + parity_position + 1])
        if parity % 2 != 0:
            error_position += 2**i

    if error_position > 0:
        hamming_code[error_position - 1] = 1 - hamming_code[error_position - 1]
        print(f"Ошибка найдена и исправлена в позиции: {error_position}")
    else:
        print("Ошибок не обнаружено.")
    
    return hamming_code

def extend_hamming_code(hamming_code):
    # Добавляем бит четности в начало кода
    parity_bit = sum(hamming_code) % 2
    extended_code = [parity_bit] + hamming_code
    return extended_code

# Пример использования
M = 832
r = 5
hamming_code = generate_hamming_code(M, r)
print(f"Классический код Хэмминга: {''.join(map(str, hamming_code))}")

# Введение ошибки в позицию 5 (индексация с 0)
hamming_code_with_error = introduce_error(hamming_code.copy(), 4)
print(f"Код Хэмминга с ошибкой: {''.join(map(str, hamming_code_with_error))}")

# Обнаружение и исправление ошибки
corrected_code = detect_and_fix_error(hamming_code_with_error, r)
print(f"Исправленный код Хэмминга: {''.join(map(str, corrected_code))}")

if (hamming_code == corrected_code):
    print("Исправлено")
else:
    print("Не исправлено")