#include <iostream>
#include <vector>

// 2 класса HammingBasic для нахождения 1 ошибки и исправления её; HammingExtension для нахождения 2-ух и более ошибок

namespace lab {
    class HammingBasic {
        public:
        HammingBasic(int M, int r, bool status);
        ~HammingBasic() = default;

        void encode(bool status); // зашифровать в нужный вид(изначально цифары -> биты - 1010101 и тд)
        void correct(); // исправить ошибку
        int decode(); // вернуть в циферный вид из битового
        void print(); // вывести
        void SetCode(int i); // по индексу сделать операцию xor с битом, тобишь поменять значение её(было 1 ксорим с 1 станет 0, было 0 ксорим с 1 станет 1)

        protected:
        int M, r; // M исходное число в 10 системе, ну кароче так как мы привыкли считать; r количество проверочных бит
        std::vector<int> code; // битовое представление числа

        private:
        bool isPowered(int x);
        int calculate();
    };

    class HammingExtension : public HammingBasic { // с этим классом тоже самое + я взял методы из предыдущего класса, наследовался кароч
        public:
        HammingExtension(int M, int r, bool status);
        ~HammingExtension() = default;

        void correct2();

        private:
        bool detect2(int &error1, int &error2);
    };
}

namespace lab {
    HammingBasic::HammingBasic(int M, int r, bool status) : M(M), r(r) {
        encode(status);
    }

    void HammingBasic::encode(bool status) {
        int k = calculate();
        int n = k + r;

        if(status) {
            code.resize(8, 0);
        } else {
            code.resize(n, 0);
        }            

        int j = 0;
        for(int i = 0; i < n; ++i) {
            if(isPowered(i + 1))
                continue;
            
            code[i] = (M >> j) & 1;
            ++j;
        }

        for(int i = 0; i < r; ++i) {
            int pos = (1 << i) - 1;
            int sum = 0;

            for(int j = 0; j < n; ++j) {
                if((j + 1) & (1 << i))
                    sum ^= code[j];
            }
            code[pos] = sum;
        }
    }

    void HammingBasic::correct() {
        int n = code.size() - 1;
        int err = 0;

        for(int i = 0; i < r; ++i) {
            int pos = (1 << i);
            int sum = 0;

            for(int j = 0; j < n; ++j) {
                if((j + 1) & pos)
                    sum ^= code[j];
            }

            if(sum != 0)
                err += pos;
        }

        if(err != 0) {
            std::cout << "Err pos: " << err - 1 << std::endl;
            code[err - 1] ^= 1;
        } else {
            std::cout << "No err" << std::endl;
        }
    }

    int HammingBasic::decode() {
        int decoded = 0;
        int j = 0;

        for(int i = 0; i < code.size(); ++i) {
            if(!isPowered(i + 1)) {
                decoded |= (code[i] << j);
                ++j;
            }
        }

        return decoded;
    }

    void HammingBasic::print() {
        for(int i = code.size() - 1; i >= 0; --i) {
            std::cout << code[i];
        } 
        std::cout << std::endl;
    }

    void HammingBasic::SetCode(int i) {
        if(i >= code.size() || i < 0) {
            std::cout << "wrong index" << std::endl;
            return;
        }
        code[i] ^= 1;
    }

    bool HammingBasic::isPowered(int x) {
        return x && (!(x & (x - 1)));
    }

    int HammingBasic::calculate() {
        int k = 0;
        int m = M;
        while(m > 0) {
            m >>= 1;
            k++;
        }
        return k;
    }

    HammingExtension::HammingExtension(int M, int r, bool status) : HammingBasic(M, r, status) {}

    void HammingExtension::correct2() {
        int n = code.size();
        int err = 0;
        int parityCheck = 0;

        for(int i = 0; i < r; ++i) {
            int pos = (1 << i);
            int sum = 0;

            for(int j = 0; j < n; ++j) {
                if((j + 1) & pos)
                    sum ^= code[j];
            }

            if(sum != 0) {
                err += pos;
                parityCheck = 1;
            }
        }

        if(err == 0) {
            std::cout << "No error detected." << std::endl;
        } else if (parityCheck && detect2(err, parityCheck)) {
            std::cout << "Double error detected at positions: " << err << " and " << parityCheck << ". Correction not possible." << std::endl;
        } else {
            std::cout << "Single error detected at position: " << err - 1 << ". Correcting..." << std::endl;
            code[err - 1] ^= 1;
        }
    }

    bool HammingExtension::detect2(int &error1, int &error2) {
        int parityCheck = 0;
        for (int i = 0; i < code.size(); ++i) {
            parityCheck ^= code[i];
        }

        if (parityCheck) {
            error2 = error1 ^ parityCheck;
            return true;
        }
        return false;
    }
}

// Первое задание: программа выводит +- всё, число в виде битов, число в битовом виде с ошибкой(1 бит не правильный), потом ошибку индексом, потом восстановленное число, потом перевод обратно в 10 систему
// Второе задание с двумя ошибками которое: там поменьше вывода, но +- тоже самое
// Одну ошибку ты узнаешь как находить, по поводу двух. Смотрится на две вещи первое отдаёт ли алгоритм какую-то ошибку + бит чётности(эта такая штука, которая говорит сколько 1 есть в битовом представлении числа, то есть если 3 единицы и все остальные 0, то бит чётности равен 1, и наобрато)
int main() {
    lab::HammingBasic quest1(853, 5, false); // тут r не трогать иначе не пашет, видимо 4 бит для проверки твоего числа не достаточно, можешь так и сказать и запустить, сказать мол говно вариант

    std::cout << "code word: ";
    quest1.print();

    std::cout << "Set err on index: ";
    quest1.SetCode(1);
    quest1.print();

    quest1.correct();
    std::cout << "Print recovery bits: ";
    quest1.print();

    std::cout << "Print encode number: " << quest1.decode() << std::endl;

    std::cout << "----------------------------------------" << std::endl;

    lab::HammingExtension quest2(748, 4, true);
    
    std::cout << "code word: ";
    quest2.print();

    std::cout << "Set err on index: ";
    quest2.SetCode(4);
    quest2.SetCode(2);
    quest2.print();

    quest2.correct2();

    std::cout << "Print encode number: " << quest2.decode() << std::endl;
}