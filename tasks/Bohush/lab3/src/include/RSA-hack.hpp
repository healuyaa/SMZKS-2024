#pragma once

#include <openssl/bn.h>
#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/err.h>

#include <vector>
#include <string>

namespace RSA_h {
    class Tools {
        public:
        Tools(std::string N, std::string e, std::vector<std::string> blocks);
        ~Tools();

        void decrypt_rsa();
        void print();

        private:
        std::vector<BIGNUM*> encrypted_blocks;
        BIGNUM* N;
        BIGNUM* e;

        std::string hex;

        void BN_sqrt_manual(BIGNUM* result, const BIGNUM* N, BN_CTX* ctx);
        void factorize_N(const BIGNUM* N, BIGNUM*& p, BIGNUM*& q);

        std::string hex_to_utf8();
    };
}