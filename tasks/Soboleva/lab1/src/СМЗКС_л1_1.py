def decimal_to_binary(n):
    """Перевод десятичного числа в двоичное представление."""
    return bin(n)[2:]

def calculate_parity_bits_positions(r):
    """Определение позиций проверочных битов в коде Хемминга."""
    return [2 ** i for i in range(r)]

def generate_hamming_code(data_bits, r):
    """Генерация кода Хемминга с проверочными битами."""
    m = len(data_bits)  # Количество информационных битов
    positions = calculate_parity_bits_positions(r)  # Позиции проверочных битов
    code_length = m + r  # Общая длина кодового слова
    code = [0] * code_length  # Инициализация кодового слова нулями

    j = 0  # Индекс для прохода по информационным битам
    # Заполнение кодового слова информационными битами
    for i in range(1, code_length + 1):
        if i in positions:
            continue  # Пропуск позиций, отведенных под проверочные биты
        if j < m:  # Проверяем, что индекс не выходит за пределы data_bits
            try:
                code[i - 1] = int(data_bits[j])  # Заполняем информационные биты
            except IndexError:
                print(f"Ошибка индекса при добавлении информационного бита: i = {i}, j = {j}")
            j += 1

    # Вычисление значений проверочных битов
    for position in positions:
        parity = 0
        for i in range(1, code_length + 1):
            if i & position:
                parity ^= code[i - 1]
        code[position - 1] = parity

    return code

def introduce_error(code):
    """Внесение ошибки в случайный бит кодового слова."""
    import random
    if not code:
        raise ValueError("Код Хемминга пуст. Ошибка при генерации кода.")
    error_position = random.randint(0, len(code) - 1)
    code[error_position] ^= 1  # Инвертируем бит для внесения ошибки
    print(f"Ошибка внесена в позицию: {error_position + 1}")
    return code, error_position + 1

def detect_and_correct_error(code, r):
    """Обнаружение и исправление ошибки в коде Хемминга."""
    positions = calculate_parity_bits_positions(r)
    error_position = 0

    # Определение позиции ошибки по проверочным битам
    for position in positions:
        parity = 0
        for i in range(1, len(code) + 1):
            if i & position:
                parity ^= code[i - 1]
        if parity != 0:
            error_position += position

    if error_position == 0:
        print("Ошибок не обнаружено.")
    else:
        print(f"Обнаружена ошибка в позиции: {error_position}")
        code[error_position - 1] ^= 1
        print("Ошибка исправлена.")

    return code

# Исходные данные
M = 590
r = 4

# 1. Перевод в двоичное представление
binary_data = decimal_to_binary(M)
print(f"Двоичное представление M ({M}): {binary_data}")

# 2. Генерация кода Хемминга
hamming_code = []  # Инициализация переменной перед использованием
try:
    hamming_code = generate_hamming_code(binary_data, r)
    if not hamming_code:
        raise ValueError("Не удалось сгенерировать код Хемминга.")
    print(f"Код Хемминга: {''.join(map(str, hamming_code))}")
except IndexError as e:
    print(f"Ошибка при генерации кода Хемминга: {e}")
except ValueError as e:
    print(e)

# 3. Внесение ошибки (проверяем, что код сгенерирован)
if hamming_code:
    try:
        code_with_error, error_position = introduce_error(hamming_code.copy())
        print(f"Код с ошибкой: {''.join(map(str, code_with_error))}")
    except ValueError as e:
        print(e)

# 4. Обнаружение и исправление ошибки
if hamming_code:
    corrected_code = detect_and_correct_error(code_with_error, r)
    print(f"Исправленный код: {''.join(map(str, corrected_code))}")
