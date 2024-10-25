#pragma once

#include "hamming.hpp"

#include <iostream>

class DoHamming {
    public:
    static void run() {
        lab::HammingBasic quest1(748, 5, false);

        std::cout << "code word: ";
        quest1.print();

        std::cout << "Set err on index: ";
        quest1.SetCode(2);
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
};