import numpy as np
import random

def text_to_binary(text):
    binary_message = ''.join(format(ord(char), '08b') for char in text)
    return binary_message

def calculate_r(m):
    r = 1
    while (2 ** r) < (m + r + 1):
        r += 1
    return r

def build_hamming_matrix(m, r):
    n = m + r  
    H = np.zeros((r, n), dtype=int)

    for i in range(1, n + 1):
        for j in range(r):
            if (i & (1 << j)) == 0:  
                H[j][i - 1] = 0
            else:
                H[j][i - 1] = 1

    return H

def calculate_redundant_bits(binary_message, H):
    m = len(binary_message)
    r = H.shape[0]
    redundant_bits = np.zeros(r, dtype=int)

    for i in range(r):
        for j in range(m):
            if H[i][j] == 1:
                redundant_bits[i] ^= int(binary_message[j]) 

    return redundant_bits

def introduce_errors(binary_message, num_errors):
    message_list = list(binary_message)
    length = len(message_list)
    
    if num_errors > 0:
        error_positions = random.sample(range(length), num_errors)
    
        for pos in error_positions:
            message_list[pos] = '1' if message_list[pos] == '0' else '0'  
        
        return ''.join(message_list), error_positions
    else:
        return binary_message, []

def calculate_syndrome(H, received_message):
    received_vector = np.array([int(bit) for bit in received_message])
    syndrome = np.dot(H, received_vector) % 2
    return syndrome

def correct_single_error(corrupted_message, syndrome):
    error_position = int(''.join(map(str, syndrome[::-1])), 2) 
    if error_position > 0:
        corrected_message = list(corrupted_message)
        corrected_message[error_position - 1] = '1' if corrected_message[error_position - 1] == '0' else '0'
        return ''.join(corrected_message), error_position
    return corrupted_message, None

def decode_message(coded_message, r):
    decoded_bits = []
    for i in range(len(coded_message)):
        if not is_power_of_two(i + 1):
            decoded_bits.append(coded_message[i])
    return ''.join(decoded_bits)

def is_power_of_two(x):
    return x and not (x & (x - 1))

text_message = "Hello, world!"

binary_message = text_to_binary(text_message)

if len(binary_message) < 16:
    print("Сообщение слишком короткое для выполнения задания")
else:
    print(f"Бинарное представление сообщения: {binary_message}")
    print(f"Длина сообщения в битах: {len(binary_message)}")
    
    m = len(binary_message)
    r = calculate_r(m)
    print(f"Число контрольных бит (r): {r}")

    H = build_hamming_matrix(m, r)
    print("Проверочная матрица Хемминга (H):")
    print(H)

    full_message = list(binary_message) + [0] * r
    redundant_bits = calculate_redundant_bits(binary_message, H)

    full_message[-r:] = redundant_bits.tolist()

    coded_message = ''.join(map(str, full_message))
    print(f"Кодовое слово с избыточными символами: {coded_message}")

    num_errors = random.choice([0, 1, 2])
    print(f"Сгенерировано число ошибок: {num_errors}")

    corrupted_message, error_positions = introduce_errors(coded_message, num_errors)
    print(f"Сообщение с ошибками: {corrupted_message} (ошибки в позициях: {error_positions})")

    syndrome = calculate_syndrome(H, corrupted_message)
    print(f"Синдром: {syndrome}")

    if np.any(syndrome):
        corrected_message, error_position = correct_single_error(corrupted_message, syndrome)
        if error_position is not None:
            print(f"Исправленное сообщение: {corrected_message}, ошибка в позиции: {error_position}")
        else:
            print("Одиночная ошибка не найдена.")
    else:
        print("Ошибок не обнаружено.")

    if num_errors == 2:
        print("Обнаружены 2 ошибки, исправление невозможно.")
    else:
        decoded_message = decode_message(corrected_message, r)
        print(f"Декодированное сообщение: {decoded_message}")
