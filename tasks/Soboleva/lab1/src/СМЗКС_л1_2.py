import random


def decimal_to_binary(n, length):
    """Перевод десятичного числа в двоичное представление с фиксированной длиной."""
    binary_str = bin(n)[2:]  # Получаем двоичное представление без префикса '0b'
    return binary_str.zfill(length)  # Дополняем до нужной длины нулями слева


def calculate_parity_bits_positions(r):
    """Определение позиций проверочных битов в коде Хемминга."""
    return [2 ** i for i in range(r)]


def generate_hamming_code_11_7(data_bits):
    """Генерация кода Хемминга (11,7) с проверочными битами."""
    m = len(data_bits)  # Количество информационных битов (7)
    r = 4  # Количество проверочных битов для кода (11,7)
    positions = calculate_parity_bits_positions(r)  # Позиции проверочных битов: 1, 2, 4, 8
    code_length = m + r  # Общая длина кодового слова: 11
    code = [0] * code_length  # Инициализация кодового слова нулями

    j = 0  # Индекс для прохода по информационным битам
    # Заполнение кодового слова информационными битами
    for i in range(1, code_length + 1):
        if i in positions:
            continue  # Пропуск позиций, отведенных под проверочные биты
        code[i - 1] = int(data_bits[j])  # Заполняем информационные биты
        j += 1

    # Вычисление значений проверочных битов
    for position in positions:
        parity = 0
        for i in range(1, code_length + 1):
            if i & position:  # Проверяем, участвует ли бит в проверке для данного проверочного бита
                parity ^= code[i - 1]  # Вычисляем четность
        code[position - 1] = parity  # Устанавливаем значение проверочного бита

    return code


def introduce_two_errors(code):
    """Внесение двух ошибок в случайные биты кодового слова."""
    if len(code) < 2:
        raise ValueError("Код слишком короткий для внесения двух ошибок.")
    error_positions = random.sample(range(len(code)), 2)  # Две случайные позиции для ошибок
    for pos in error_positions:
        code[pos] ^= 1  # Инвертируем бит для внесения ошибки
    print(f"Ошибки внесены в позиции: {[pos + 1 for pos in error_positions]}")
    return code, [pos + 1 for pos in error_positions]


def detect_errors(code, r):
    """Обнаружение всех ошибок в коде Хемминга (11,7)."""
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

    return error_position


def find_two_errors(code, r):
    """Попытка обнаружения двух ошибок с помощью перебора."""
    original_error_position = detect_errors(code, r)
    if original_error_position == 0:
        print("Ошибок не обнаружено.")
        return []

    # Пробуем найти комбинации ошибок
    possible_errors = []
    for i in range(len(code)):
        for j in range(i + 1, len(code)):
            modified_code = code.copy()
            modified_code[i] ^= 1
            modified_code[j] ^= 1
            if detect_errors(modified_code, r) == 0:
                possible_errors.append((i + 1, j + 1))

    if possible_errors:
        print(f"Найдены возможные позиции двух ошибок: {possible_errors}")
    else:
        print("Не удалось найти две ошибки.")
    return possible_errors


def correct_errors(code, error_positions):
    """Исправление двух ошибок."""
    if not error_positions:
        print("Ошибки не обнаружены для исправления.")
        return code

    for pos in error_positions:
        code[pos - 1] ^= 1  # Исправляем ошибки
        print(f"Ошибка исправлена в позиции: {pos}")

    return code


# Исходные данные
M = 590  # Пример числа (в двоичном виде: 1011010)
binary_data = decimal_to_binary(M, 7)  # Приведение длины до 7 бит (информационные биты)

print(f"Двоичное представление числа M ({M}): {binary_data}")

# Генерация кода Хемминга (11,7)
hamming_code = generate_hamming_code_11_7(binary_data)
print(f"Код Хемминга (11,7): {''.join(map(str, hamming_code))}")

# Внесение двух ошибок
code_with_two_errors, error_positions = introduce_two_errors(hamming_code.copy())
print(f"Код с двумя ошибками: {''.join(map(str, code_with_two_errors))}")

# Обнаружение двух ошибок
found_errors = find_two_errors(code_with_two_errors, 4)

# Исправление ошибок
if found_errors:
    corrected_code = correct_errors(code_with_two_errors, found_errors[0])
    print(f"Код после исправления: {''.join(map(str, corrected_code))}")
else:
    print("Исправление не удалось.")
