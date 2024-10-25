#pragma once

#include <vector>

namespace lab {
    class HammingBasic {
        public:
        HammingBasic(int M, int r, bool status);
        ~HammingBasic() = default;

        void encode(bool status);
        void correct();
        int decode();
        void print();
        void SetCode(int i);

        protected:
        int M, r;
        std::vector<int> code;

        private:
        bool isPowered(int x);
        int calculate();
    };

    class HammingExtension : public HammingBasic {
        public:
        HammingExtension(int M, int r, bool status);
        ~HammingExtension() = default;

        void correct2();

        private:
        bool detect2(int &error1, int &error2);
    };
}