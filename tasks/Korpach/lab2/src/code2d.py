import numpy as np

def add_errors(binary_word, num_errors):
    error_indices = np.random.choice(len(binary_word), size=num_errors, replace=False)
    binary_word_with_errors = binary_word.copy()
    binary_word_with_errors[error_indices] = np.bitwise_xor(binary_word_with_errors[error_indices], 1)
    return binary_word_with_errors, error_indices

class IterativeCode:
    def __init__(self, length, rows, cols, n_parities):
        self.length = length
        self.rows = rows
        self.cols = cols
        self.n_parities = n_parities
        self.word = self.generate_word()
        self.matrix = self.word2matrix()
        self.parities = self.calculate_parities()

    def generate_word(self):
        return np.random.randint(2, size=self.length)

    def word2matrix(self):
        return self.word.reshape((self.rows, self.cols))  # type: ignore

    def calculate_parities(self):
        parities = {}
        if self.n_parities >= 2:
            parities['row'] = np.sum(self.matrix, axis=1) % 2
            parities['col'] = np.sum(self.matrix, axis=0) % 2
        if self.n_parities >= 3:
            parities['diag_down'] = self.calculate_diagonal_parity_down()
        if self.n_parities >= 4:
            parities['diag_up'] = self.calculate_diagonal_parity_up()
        if self.n_parities == 5:
            parities['overall'] = self.calculate_global_parity(parities)
        return parities

    def calculate_diagonal_parity_down(self):
        flipped_matrix = np.fliplr(self.matrix)
        parities = [np.sum(np.diagonal(flipped_matrix, offset=offset)) % 2 
                    for offset in range(-(self.rows - 1), self.cols)]
        return np.array(parities)[::-1]

    def calculate_diagonal_parity_up(self):
        parities = [np.sum(np.diagonal(self.matrix, offset=offset)) % 2 
                    for offset in range(-(self.rows - 1), self.cols)]
        return np.array(parities)

    def calculate_global_parity(self, parities):
        all_parity_bits = np.concatenate([parity for parity in parities.values() if isinstance(parity, np.ndarray)])
        return np.array([np.sum(all_parity_bits) % 2])

    def get_indices(self, kind, index):
        if kind == 'row':
            return [(index, col_idx) for col_idx in range(self.matrix.shape[1])]
        elif kind == 'col':
            return [(row_idx, index) for row_idx in range(self.matrix.shape[0])]
        elif kind == 'diag_down':
            return self.get_diagonal_indices_down(index)
        elif kind == 'diag_up':
            return self.get_diagonal_indices_up(index)

    def get_diagonal_indices_up(self, parity_index):
        offset = parity_index - (self.rows - 1)
        diag = np.diagonal(self.matrix, offset=offset)
        if offset >= 0:
            return [(i, i + offset) for i in range(len(diag))]
        else:
            return [(i - offset, i) for i in range(len(diag))]

    def get_diagonal_indices_down(self, parity_index):
        indices = self.get_diagonal_indices_up(parity_index)
        return [(self.rows - 1 - index[0], index[1]) for index in indices]

    def __str__(self):
        return (f"Слово: {self.word}\n" +
                f"Матрица:\n {self.matrix}\n" +
                f"Паритеты строк: {self.parities.get('row')}\n" +
                f"Паритеты столбцов: {self.parities.get('col')}\n" +
                f"Паритеты диагонали (вниз): {self.parities.get('diag_down')}\n" +
                f"Паритеты диагонали (вверх): {self.parities.get('diag_up')}\n" +
                f"Паритет паритетов: {self.parities.get('overall')}")

class IterativeCodeSend(IterativeCode):
    def combine_parities_and_word(self):
        parities_array = [self.word]
        for key in list(self.parities.keys()):
            parities_array.append(self.parities[key])
        return np.concatenate(parities_array)

class IterativeCodeReceive(IterativeCode):
    def __init__(self, length, rows, cols, n_parities, word):
        super().__init__(length, rows, cols, n_parities)
        self.unpack(word)
        self.matrix = self.word2matrix()
        self.parities = self.calculate_parities()
        self.errors = self.find_errors()

    def unpack(self, word):
        splits = [
            self.length,
            self.length + self.rows,
            self.length + self.rows + self.cols,
            self.length + self.rows + self.cols + (self.cols + self.rows - 1),
            self.length + self.rows + self.cols + 2 * (self.cols + self.rows - 1),
        ]
        
        self.word = word[:splits[0]]
        self.current_parities = {}

        if self.n_parities >= 2:
            self.current_parities['row'] = word[splits[0]:splits[1]]
            self.current_parities['col'] = word[splits[1]:splits[2]]
        if self.n_parities >= 3:
            self.current_parities['diag_down'] = word[splits[2]:splits[3]]
        if self.n_parities >= 4:
            self.current_parities['diag_up'] = word[splits[3]:splits[4]]
        if self.n_parities == 5:
            self.current_parities['overall'] = word[-1]

    def find_errors(self):
        errors = {}
        for key in list(self.parities.keys()):
            if key == 'overall':
                continue
            errors_in_parities = np.where(self.current_parities[key] != self.parities[key])[0].tolist()
            for error_index in errors_in_parities:
                errors[key] = set()
                for position in self.get_indices(key, error_index):
                    errors[key].add(position)

        if len(errors.keys()) < self.n_parities - 1:
            return set()
        return set.intersection(*errors.values())

    def fix_errors(self):
        if not self.errors:
            return self.word
        matrix = self.matrix.copy()
        for x, y in self.errors:
            matrix[x][y] ^= 1
        return matrix.flatten()

    def __str__(self):
        return (super().__str__() + 
                f"\nНайденные ошибки: {self.errors}\n" + 
                f"Исправленное слово: {self.fix_errors()}")

if __name__ == "__main__":
    length = 40
    rows, cols = 5, 8
    num_parities = 5  # можно менять значение для тестирования
    num_errors = 1

    code2send = IterativeCodeSend(length, rows, cols, num_parities)
    print(code2send)

    word2send = code2send.combine_parities_and_word()
    print("Слово с паритетами:", word2send)
    word2send, _ = add_errors(word2send, num_errors)
    print("Слово с ошибками:", word2send)

    code2receive = IterativeCodeReceive(length, rows, cols, num_parities, word2send)
    print(code2receive)
