#include "iterative_codes.hpp"

#include <iostream>

enum class Type {
    SQUARE = 0,
    RECTANGLE = 1,
    MULTIPLELAYERS = 2
};
namespace lab {
    class App {
        public:
        static void run() {
            code::Iteratives app(60505, code::SIZES::size_square, code::Paritets::three);
            code::Multiple app_m(60505, code::LayersVariable::four_two, code::Paritets::five);

            Type run = Type::SQUARE;

            switch (run) {
                case Type::SQUARE:
                    app.encodeSquare();

                    std::cout << "Matrix: " << std::endl;
                    app.printSquare();
                    std::cout << "-----------------------------" << std::endl;

                    app.SetCode(1, 1);
                    app.SetCode(1, 2);
                    app.SetCode(1, 3);

                    std::cout << "Matrix with err: " << std::endl;
                    app.printSquare();

                    std::cout << "-----------------------------" << std::endl;
                    std::cout << "Find err: " << std::endl;
                    app.decodeSquare();

                    std::cout << "-----------------------------" << std::endl;
                    std::cout << "Correct matrix: " << std::endl;
                    app.printSquare();
                    std::cout << "---------------------------------------------------------------------------------------" << std::endl;                
                break;

            case Type::RECTANGLE:
                app.encodeRectangle();
                
                std::cout << "Matrix: " << std::endl;
                app.printRectangle();
                std::cout << "-----------------------------" << std::endl;

                app.SetCode(1, 1);
                app.SetCode(1, 2);
                app.SetCode(1, 3);

                std::cout << "Matrix with err: " << std::endl;
                app.printRectangle();

                std::cout << "-----------------------------" << std::endl;
                std::cout << "Find err: " << std::endl;
                app.decodeRectangle();

                std::cout << "-----------------------------" << std::endl;
                std::cout << "Correct matrix: " << std::endl;
                app.printRectangle();
                std::cout << "---------------------------------------------------------------------------------------" << std::endl;
            break;

            case Type::MULTIPLELAYERS:
                app_m.encodeMultiple();
                app_m.printMultiple();
                app_m.SetCode(0, 0);
                app_m.SetCode(1, 1);
                app_m.decodeMultiple();
                app_m.printMultiple();
            break;
            }
        }
    };
}