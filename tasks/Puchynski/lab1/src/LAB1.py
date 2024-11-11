import numpy as np
import random

def decimal_to_binary(num):
    return format(num, 'b').zfill(16) 

def create_hamming_matrix(total_bits, r):
    matrix = []
    for i in range(1, total_bits + 1):
        binary = format(i, '0' + str(total_bits) + 'b') 
        row = []
        for j in range(total_bits):
            if binary[j] == '1':
                row.append(1)
            else:
                row.append(0)
        matrix.append(row)
    return np.array(matrix).T

def add_parity_bits(data, r):
    n = len(data)
    total_bits = n + r
    coded_message = [0] * total_bits
    
    j = 0 
    for i in range(1, total_bits + 1):
        if (i & (i - 1)) == 0:
            coded_message[i - 1] = 0 
        else:
            coded_message[i - 1] = int(data[j])
            j += 1
    
    for i in range(r):
        parity_bit_position = 2**i
        parity_value = 0
        for j in range(1, total_bits + 1):
            if j & parity_bit_position:
                parity_value ^= coded_message[j - 1]
        coded_message[parity_bit_position - 1] = parity_value
    
    return coded_message

def introduce_errors(data, num_errors=1):
    data_with_errors = data.copy()
    error_positions = random.sample(range(len(data)), num_errors)
    for pos in error_positions:
        data_with_errors[pos] ^= 1 
    return data_with_errors, error_positions

def calculate_syndrome(H, received_message):
    return np.dot(H, received_message) % 2

def correct_error(received_message, syndrome):
    syndrome_value = int(''.join(map(str, syndrome)), 2)
    if syndrome_value > 0 and syndrome_value <= len(received_message):
        received_message[syndrome_value - 1] ^= 1
    return received_message

def hamming_classic(M, r=4, num_errors=1):
    binary_message = decimal_to_binary(M)
    print(f"Исходное двоичное сообщение: {binary_message}")
    
    total_bits = len(binary_message) + r
    H = create_hamming_matrix(total_bits, r)
    
    coded_message = add_parity_bits(binary_message, r)
    print(f"Сообщение с избыточными битами: {coded_message}")
    
    received_message, error_positions = introduce_errors(coded_message, num_errors)
    print(f"Сообщение с ошибками: {received_message}")
    print(f"Позиции ошибок: {error_positions}")
    
    syndrome = calculate_syndrome(H, received_message)
    print(f"Синдром: {syndrome}")
    
    if np.any(syndrome):
        print("Ошибка обнаружена. Исправляем...")
        corrected_message = correct_error(received_message, syndrome)
        print(f"Исправленное сообщение: {corrected_message}")
    else:
        corrected_message = received_message
        print("Ошибок не обнаружено.")
    
    return corrected_message

def hamming_extended(M, num_errors=2):
    binary_message = decimal_to_binary(M)[:7] 
    print(f"Исходное двоичное сообщение (расширенный): {binary_message}")
    
    r = 3 
    total_bits = len(binary_message) + r
    H = create_hamming_matrix(total_bits, r)
    
    coded_message = add_parity_bits(binary_message, r)
    print(f"Сообщение с избыточными битами (расширенный): {coded_message}")
    
    received_message, error_positions = introduce_errors(coded_message, num_errors)
    print(f"Сообщение с ошибками (расширенный): {received_message}")
    print(f"Позиции ошибок (расширенный): {error_positions}")
    
    syndrome = calculate_syndrome(H, received_message)
    print(f"Синдром (расширенный): {syndrome}")
    
    if np.any(syndrome):
        print("Ошибки обнаружены. Исправляем...")
        corrected_message = correct_error(received_message, syndrome)
        print(f"Исправленное сообщение (расширенный): {corrected_message}")
    else:
        corrected_message = received_message
        print("Ошибок не обнаружено.")
    
    return corrected_message

M = 774
r = 4
num_errors_classic = 1
num_errors_extended = 2


print("Классический алгоритм Хемминга:")
corrected_message_classic = hamming_classic(M, r, num_errors_classic)

print("\nРасширенный алгоритм Хемминга:")
corrected_message_extended = hamming_extended(M, num_errors_extended)
