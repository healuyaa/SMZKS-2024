#pragma once

#include "RSA-hack.hpp"
#include <vector>

namespace lab {
    class App {
        public:
        static void run() {
            RSA_h::Tools quest("99595193774911", "1908299", std::vector<std::string>{
                "75790643190143",
                "36869061035180",
                "38422576553598",
                "68899435645717",
                "16193161920958",
                "98487458352335",
                "34167725433806",
                "96613844267045",
                "26583768908805",
                "73052827576371",
                "94695336463618",
                "69092596694070",
            });

            quest.decrypt_rsa();
            quest.print();

            quest.~Tools();
        }
    };
}