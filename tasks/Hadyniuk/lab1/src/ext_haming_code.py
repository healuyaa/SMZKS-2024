import numpy as np

def generate_hamming_code(M, r):
    # Переводим число в двоичный формат
    binary_M = bin(M)[2:].zfill(4)[:4]  # Обрезаем до 4 бит
    M_bits = len(binary_M)
    n = min(M_bits + r, 7)  # Ограничиваем код до 7 бит
    hamming_code = [0] * n

    j = 0
    for i in range(n):
        if (i + 1) & i == 0:
            continue
        if j < M_bits:
            hamming_code[i] = int(binary_M[j])
            j += 1

    def calculate_parity_bits(code, r):
        n = len(code)
        for i in range(r):
            parity_position = 2**i - 1
            if parity_position >= n:
                break  # Если проверочный бит выходит за границы 7 бит
            parity = 0
            for j in range(parity_position, n, 2 * (parity_position + 1)):
                parity ^= sum(code[j:j + parity_position + 1])
            code[parity_position] = parity % 2
        return code

    hamming_code = calculate_parity_bits(hamming_code, r)
    return hamming_code

def introduce_error(hamming_code, positions):
    for position in positions:
        if position < len(hamming_code):
            hamming_code[position] = 1 - hamming_code[position]
    return hamming_code

def detect_and_fix_error(hamming_code, r):
    n = len(hamming_code)
    error_position = 0

    for i in range(r):
        parity_position = 2**i - 1
        if parity_position >= n:
            break  # Если проверочный бит выходит за границы 7 бит
        parity = 0
        for j in range(parity_position, n, 2 * (parity_position + 1)):
            parity ^= sum(hamming_code[j:j + parity_position + 1])
        if parity % 2 != 0:
            error_position += 2**i

    if error_position > 0 and error_position <= n:
        hamming_code[error_position - 1] = 1 - hamming_code[error_position - 1]
        print(f"Ошибка найдена и исправлена в позиции: {error_position}")
    else:
        print("Ошибок не обнаружено.")
    
    return hamming_code

def extend_hamming_code(hamming_code):
    parity_bit = sum(hamming_code) % 2
    extended_code = [parity_bit] + hamming_code[:6]  # Ограничиваем до 7 бит
    return extended_code

def detect_two_errors(hamming_code, r):
    n = len(hamming_code)
    error_positions = []
    
    # Вычисляем синдром для поиска позиций ошибок
    for i in range(r):
        parity_position = 2**i - 1
        if parity_position >= n:
            break  # Если проверочный бит выходит за границы 7 бит
        parity = 0
        for j in range(parity_position, n, 2 * (parity_position + 1)):
            parity ^= sum(hamming_code[j:j + parity_position + 1])
        if parity % 2 != 0:
            error_positions.append(parity_position + 1)
    
    if len(error_positions) > 0:
        print(f"Обнаружены ошибки в позициях: {error_positions}")
    else:
        print("Ошибок не обнаружено.")

    return error_positions

# Пример использования
M = 832
r = 3
hamming_code = generate_hamming_code(M, r)
print(f"Классический код Хэмминга: {''.join(map(str, hamming_code))}")

# Введение одной ошибки
hamming_code_with_error = introduce_error(hamming_code.copy(), [2])
print(f"Код Хэмминга с одной ошибкой: {''.join(map(str, hamming_code_with_error))}")

# Обнаружение и исправление одной ошибки
corrected_code = detect_and_fix_error(hamming_code_with_error, r)
print(f"Исправленный код Хэмминга: {''.join(map(str, corrected_code))}")

# Введение двух ошибок
hamming_code_with_two_errors = introduce_error(hamming_code.copy(), [0 ,1])
print(f"Код Хэмминга с двумя ошибками: {''.join(map(str, hamming_code_with_two_errors))}")

# Обнаружение двух ошибок
detected_errors = detect_two_errors(hamming_code_with_two_errors, r)
