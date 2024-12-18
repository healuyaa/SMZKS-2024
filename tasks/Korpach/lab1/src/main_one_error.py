def get_parity_bit(data, parity_position):
    """Вычисляет значение контрольного бита для заданной позиции."""
    parity_bit = 0
    for i in range(parity_position - 1, len(data), 2 * parity_position):
        parity_bit ^= sum(data[i:i + parity_position])
    return parity_bit % 2

def hamming_encode(number):
    """Кодирует число с использованием алгоритма Хэмминга."""
    data = list(map(int, bin(number)[2:].zfill(7))) 
    print(f"Исходные данные в битах: {data}")
    
    m = len(data)
    r = 0
    while (2**r) < (m + r + 1):
        r += 1

    encoded_data = [0] * (m + r)
    j = 0
    for i in range(len(encoded_data)):
        if (i + 1) & (i) == 0:
            # Позиции для контрольных битов
            encoded_data[i] = 0
        else:
            encoded_data[i] = data[j]
            j += 1
    
    print(f"Последовательность с нулевыми контрольными битами: {encoded_data}")
    
    # Вычисляем значения контрольных битов
    for i in range(r):
        parity_position = 2 ** i
        encoded_data[parity_position - 1] = get_parity_bit(encoded_data, parity_position)
    
    return encoded_data

def hamming_decode(encoded_data):
    # Определяем количество контрольных битов
    m = len(encoded_data)
    r = 0
    while (2**r) < m + 1:
        r += 1

    error_position = 0
    for i in range(r):
        parity_position = 2 ** i
        if get_parity_bit(encoded_data, parity_position) != 0:
            error_position += parity_position
    
    if error_position > 0:
        print(f"Обнаружена ошибка в позиции: {error_position}")
        # Исправляем ошибку
        encoded_data[error_position - 1] ^= 1
        print(f"Исправленная последовательность: {encoded_data}")
    else:
        print("Ошибок не обнаружено.")
    
    # Удаляем контрольные биты и восстанавливаем исходные данные
    data = []
    for i in range(len(encoded_data)):
        if (i + 1) & (i) != 0:
            data.append(encoded_data[i])
    
    print(f"Восстановленные данные: {data}")
    return data

def main():
    number = int(input("Введите число для кодирования: "))
    encoded = hamming_encode(number)
    print(f"Закодированное число в формате Хэмминга: {encoded}")

    # Симулируем ошибку
    error_position = int(input("Введите позицию для внесения ошибки (или 0 для отсутствия ошибки): "))
    if error_position > 0:
        encoded[error_position - 1] ^= 1
        print(f"Последовательность с внесенной ошибкой: {encoded}")
  
    decoded = hamming_decode(encoded)
    print(f"Число после декодирования: {int(''.join(map(str, decoded)), 2)}")

if __name__ == "__main__":
    main()
