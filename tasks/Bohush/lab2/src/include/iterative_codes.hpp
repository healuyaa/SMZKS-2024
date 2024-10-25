#pragma once

#include <cstdint>
#include <memory>
#include <vector>

namespace code {
    constexpr int SIZE_BITS = 16;

    constexpr int SIZE_MATRIX_2 = 2;
    constexpr int SIZE_MATRIX_4 = 4;
    constexpr int SIZE_MATRIX_8 = 8;

    constexpr int SIZE_LAYERS = 2;

    enum class SIZES {
        size_rectangle = 2,
        size_square = 4,
    };

    enum class Paritets {
        two = 2,
        three = 3,
        four = 4,
        five = 5,
        special = 6
    };

    enum class LayersVariable {
        four_two = 0,
        two_four = 1
    };

    struct Data {
        std::vector<std::vector<std::uint8_t>> matrix;        

        std::vector<std::uint8_t> paritet_x;
        std::vector<std::uint8_t> paritet_y;
        int paritet_xy;
    };

    struct DataM {
        std::vector<std::vector<std::uint8_t>> matrix;

        std::vector<std::uint8_t> paritet_x;
        std::vector<std::uint8_t> paritet_y;
        int paritet_xy;

        std::vector<std::uint8_t> paritet_dl;
        std::vector<std::uint8_t> paritet_dr;

        std::vector<std::vector<std::uint8_t>> paritets_z;
    };

    class Iteratives {
        public:
        Iteratives(int number, SIZES size, Paritets paritet);
        ~Iteratives() = default;

        void SetCode(int i, int j);

        void encodeSquare();
        void encodeRectangle();

        void decodeSquare();
        void decodeRectangle();

        void printSquare();
        void printRectangle();

        private:
        std::unique_ptr<Data> v;
        int number;

        SIZES size;
        Paritets paritet;

        void IntToMatrix(int number);
    };

    class Multiple {
        public:
        Multiple(int number, LayersVariable variable, Paritets paritet);
        ~Multiple() = default;

        void SetCode(int i, int j);

        void encodeMultiple();
        void decodeMultiple();
        
        void printMultiple();

        private:
        std::vector<std::unique_ptr<DataM>> v;
        int number;

        LayersVariable variable;
        Paritets paritet;

        void IntToMatrix(int number);
    };
}