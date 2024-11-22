from functools import reduce

def calculate_ctrl_sum(lst, r):
    return list(
        f"{reduce(lambda x, y: x ^ y, (i + 1 for i, x in enumerate(lst) if x == '1')):0{r}b}"
    )

# Функция для инверсии элемента на заданной позиции
def invert_element(lst, index):
    lst[index] = str(int(lst[index]) ^ 1)
    return lst

# Исходное число
M = 865
r = 3

# Преобразуем число M в двоичную строку
M_binary_str = f"{M:b}"
M_lst = list(M_binary_str)
print(f"M:{M}, r:{r}\n{M_lst}")

# Определяем минимальное количество проверочных битов r
while 2 ** r > len(M_lst) + r:
    r -= 1
r += 1

# Вставляем проверочные биты (пока пустые) в нужные позиции
for p in range(r):
    M_lst.insert(2 ** p - 1, '')

print("Двоичное представление с пустыми проверочными битами:", M_lst)

# Вычисляем первую контрольную сумму для пустых проверочных битов
ctrl_sum1 = calculate_ctrl_sum(M_lst, r)[::-1]
print("Первая контрольная сумма:", ctrl_sum1)

# Заполняем проверочные биты в их позиции
M_lst = [ctrl_sum1.pop(0) if elem == '' and ctrl_sum1 else elem for elem in M_lst]
print("Код Хэмминга с заполненными проверочными битами:", M_lst, end='\n\n')

# Вычисляем контрольную сумму для проверки кода без ошибок
ctrl_sum2 = calculate_ctrl_sum(M_lst, r)
print("Контрольная сумма для проверки (без ошибок):", ctrl_sum2)
print("Код Хэмминга:", M_lst, end='\n\n')

# Инвертируем бит в позиции 5, чтобы ввести ошибку
index = 5
M_lst = invert_element(M_lst, index)
print(f"Код Хэмминга с ошибкой в позиции {index}:", M_lst)

# Вычисляем контрольную сумму для нахождения ошибки
control_sum3 = calculate_ctrl_sum(M_lst, r)
print("Контрольная сумма для проверки (с ошибкой):", control_sum3)

# Определяем индекс ошибки
error_index = int(''.join(control_sum3), 2) - 1
print(f"Ошибка найдена в позиции: {error_index}")

# Исправляем ошибку путём инверсии бита
M_lst = invert_element(M_lst, error_index)
print("Код Хэмминга после исправления ошибки:", M_lst)
