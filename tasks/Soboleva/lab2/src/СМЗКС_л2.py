'''import numpy as np
import random


# Генерация случайного двоичного слова длиной k бит
def generate_random_word(k):
    return np.random.randint(0, 2, k)


# Вычисление проверочных битов для блока с учетом групп паритетов
def calculate_parity_bits_block(block, parity_groups):
    parity_bits = []

    # Для каждой группы вычисляем сумму битов
    for group in parity_groups:
        # Уменьшаем индексы группы на 1, чтобы соответствовать индексации Python
        valid_group = [i - 1 for i in group if i - 1 < len(block)]  # Защита от выхода за границы
        parity = sum(block[i] for i in valid_group) % 2
        parity_bits.append(parity)

    return np.array(parity_bits)


# Формирование кодового слова с проверочными битами
def form_code_word(info_word, k1_groups, k2_groups, parity_groups):
    parity_bits_total = []

    # Разбиение на блоки и вычисление проверочных битов для каждого блока
    index = 0
    for i, k1 in enumerate(k1_groups):
        block = info_word[index:index + k1]
        index += k1
        parity_bits = calculate_parity_bits_block(block, parity_groups[i])
        parity_bits_total.extend(parity_bits)

    return np.concatenate((info_word, parity_bits_total))


# Внесение случайных ошибок в кодовое слово
def introduce_errors(code_word, num_errors):
    code_word_with_errors = code_word.copy()
    error_positions = random.sample(range(len(code_word)), num_errors)
    for pos in error_positions:
        code_word_with_errors[pos] ^= 1  # Инвертировать бит
    return code_word_with_errors, error_positions


# Проверка и исправление ошибок для каждого блока
def check_and_correct_errors(code_word_with_errors, k1_groups, parity_groups):
    information_word = code_word_with_errors[:20]  # Информационное слово длиной 20 бит
    parity_bits_received = code_word_with_errors[20:]

    # Пересчет проверочных битов для каждого блока
    index = 0
    for i, k1 in enumerate(k1_groups):
        block = information_word[index:index + k1]
        index += k1
        parity_bits_calculated = calculate_parity_bits_block(block, parity_groups[i])

        # Сравнение с полученными проверочными битами
        if not np.array_equal(parity_bits_calculated, parity_bits_received[i]):
            print(f"Обнаружена ошибка в блоке {i + 1}. Пытаемся исправить...")

            # Пример исправления ошибки
            for j in range(len(block)):
                test_block = block.copy()
                test_block[j] ^= 1
                if np.array_equal(calculate_parity_bits_block(test_block, parity_groups[i]), parity_bits_received[i]):
                    print(f"Исправлена ошибка на позиции {j} в блоке {i + 1}")
                    information_word[index - k1:index] = test_block
                    break
        else:
            print(f"Ошибок в блоке {i + 1} не обнаружено.")

    return np.concatenate((information_word, parity_bits_received))


# Оценка корректирующей способности
def evaluate_correction(original_word, corrected_word, num_errors):
    errors_left = sum(original_word != corrected_word)
    if errors_left == 0:
        print(f"Все {num_errors} ошибки исправлены!")
    else:
        print(f"Не удалось исправить {errors_left} ошибки.")


# Параметры задачи
k = 20  # Длина информационного слова
k1_groups = [4, 2, 2, 2]  # Подблоки для k1
k2_groups = [5, 10, 5, 2]  # Подблоки для k2
parity_groups = [
    [(2, 3)],  # Для первого блока
    [(2, 3)],  # Для второго блока
    [(2, 3, 4, 5)],  # Для третьего блока
    [(2, 3, 4, 5)]  # Для четвертого блока
]

# 1. Генерация случайного информационного слова
info_word = generate_random_word(k)
print(f"Информационное слово: {info_word}")

# 2. Формирование кодового слова
code_word = form_code_word(info_word, k1_groups, k2_groups, parity_groups)
print(f"Кодовое слово: {code_word}")

# 3. Генерация ошибок
num_errors = 1  # Внесём 2 ошибки
code_word_with_errors, error_positions = introduce_errors(code_word, num_errors)
print(f"Кодовое слово с ошибками (позиции ошибок {error_positions}): {code_word_with_errors}")

# 4. Поиск и исправление ошибок
corrected_word = check_and_correct_errors(code_word_with_errors, k1_groups, parity_groups)
print(f"Исправленное кодовое слово: {corrected_word}")

# 5. Оценка корректирующей способности
evaluate_correction(code_word, corrected_word, num_errors)'''
import numpy as np


class Iteratives:
    @staticmethod
    def list_to_matrix(bit_list, rows, cols):
        """Преобразует список двоичных значений в матрицу."""
        padded_list = bit_list + [0] * (rows * cols - len(bit_list))  # Дополняем до нужного размера
        matrix = np.array(padded_list, dtype=int).reshape((rows, cols))
        return matrix


class Multiple:
    def __init__(self, bit_list, k1_groups, k2_groups, parity_groups):
        self.bit_list = bit_list
        self.k1_groups = k1_groups
        self.k2_groups = k2_groups
        self.parity_groups = parity_groups

        self.k1_rows = len(k1_groups)
        self.k1_cols = sum(k1_groups)

        self.k2_rows = len(k2_groups)
        self.k2_cols = sum(k2_groups)

        # Инициализируем матрицы
        self.k1_matrix = Iteratives.list_to_matrix(bit_list, self.k1_rows, self.k1_cols)
        self.k2_matrix = Iteratives.list_to_matrix(bit_list, self.k2_rows, self.k2_cols)

        # Инициализация векторов четности
        self.parity_vectors_k1 = np.zeros(self.k1_rows + len(parity_groups), dtype=int)
        self.parity_vectors_k2 = np.zeros(self.k2_rows + len(parity_groups), dtype=int)

    def encode_multiple(self):
        """Кодирует данные и заполняет векторы четности."""
        # Кодируем первый блок (k1)
        for i in range(self.k1_rows):
            row_sum = np.sum(self.k1_matrix[i])
            self.parity_vectors_k1[i] = row_sum % 2  # Четность по строкам

        # Кодируем второй блок (k2)
        for i in range(self.k2_rows):
            row_sum = np.sum(self.k2_matrix[i])
            self.parity_vectors_k2[i] = row_sum % 2  # Четность по строкам

        # Заполнение дополнительных векторов четности
        for group_idx, group in enumerate(self.parity_groups):
            for indices in group:
                parity_sum_k1 = np.sum(self.parity_vectors_k1[list(indices)]) % 2
                parity_sum_k2 = np.sum(self.parity_vectors_k2[list(indices)]) % 2
                self.parity_vectors_k1[self.k1_rows + group_idx] = parity_sum_k1
                self.parity_vectors_k2[self.k2_rows + group_idx] = parity_sum_k2

    def decode_multiple(self):
        """Декодирует данные и проверяет наличие ошибок."""
        # Проверка четности для первого блока (k1)
        error_positions = []
        for i in range(self.k1_rows):
            if np.sum(self.k1_matrix[i]) % 2 != self.parity_vectors_k1[i]:
                error_positions.append(i)

        # Проверка четности для второго блока (k2)
        for i in range(self.k2_rows):
            if np.sum(self.k2_matrix[i]) % 2 != self.parity_vectors_k2[i]:
                error_positions.append(i + self.k1_rows)

        return error_positions


# Параметры задачи
k = 20  # Длина информационного слова
k1_groups = [4, 2, 2, 2]  # Подблоки для k1
k2_groups = [5, 10, 5, 2]  # Подблоки для k2
parity_groups = [
    [(0, 1)],  # Для первого блока
    [(0, 1)],  # Для второго блока
    [(0, 1, 2, 3)],  # Для третьего блока
    [(0, 1, 2, 3)]  # Для четвертого блока
]

# Пример использования с массивом двоичных значений
bit_list = [1, 0, 1, 1, 0, 0, 1, 0, 0, 1]  # Информационное слово
# Дополняем массив до 20 элементов
bit_list = bit_list + [0] * (k - len(bit_list))  # Теперь длина bit_list будет 20

encoder = Multiple(bit_list, k1_groups, k2_groups, parity_groups)

# Кодирование
encoder.encode_multiple()

# Вывод результатов
print("Матрица k1:")
print(encoder.k1_matrix)
print("Матрица k2:")
print(encoder.k2_matrix)
print("Векторы четности k1:")
print(encoder.parity_vectors_k1)
print("Векторы четности k2:")
print(encoder.parity_vectors_k2)

# Декодирование и проверка ошибок
errors = encoder.decode_multiple()
if errors:
    print("Обнаружены ошибки в позициях:", errors)
else:
    print("Ошибок не найдено.")
