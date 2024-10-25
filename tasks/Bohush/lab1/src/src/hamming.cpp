#include "hamming.hpp"

#include <iostream>

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