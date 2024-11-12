#include "RSA_hack.hpp"

#include <iostream>
#include <openssl/bn.h>
#include <openssl/crypto.h>

namespace Tools {
    RSA::RSA(std::string N, std::string e1, std::string e2, const std::vector<std::string> C1, const std::vector<std::string> C2) {
        this->N = BN_new();
        this->e1 = BN_new();
        this->e2 = BN_new();

        BN_dec2bn(&this->N, N.c_str());
        BN_dec2bn(&this->e1, e1.c_str());
        BN_dec2bn(&this->e2, e2.c_str());

        hex = "";

        this->C1.resize(SIZE);
        this->C2.resize(SIZE);

        for(int i = 0; i < SIZE; ++i) {
            this->C1[i] = BN_new();
            this->C2[i] = BN_new();

            BN_dec2bn(&this->C1[i], C1[i].c_str());
            BN_dec2bn(&this->C2[i], C2[i].c_str());
        }
    }

    RSA::~RSA() {
        for(int i = 0; i < SIZE; ++i) {
            BN_free(C1[i]);
            BN_free(C2[i]);
        }

        BN_free(N);
        BN_free(e1);
        BN_free(e2);
    }

    void RSA::hack() {
        BN_CTX* ctx = BN_CTX_new();

        BIGNUM* r = BN_new();
        BIGNUM* s = BN_new();
        BIGNUM* gcd = BN_new();
        BIGNUM* result = BN_new();

        decrypt_rsa(e1, e2, r, s, ctx);

        BIGNUM* temp1 = BN_new();
        BIGNUM* temp2 = BN_new();

        for (int i = 0; i < SIZE; ++i) {
            BN_mod_exp(temp1, C1[i], r, N, ctx);            
            BN_mod_exp(temp2, C2[i], s, N, ctx);
            
            BN_mod_mul(result, temp1, temp2, N, ctx);

            char* dec = BN_bn2dec(result);

            std::cout << "Intermediate result for index " << i << ": " << bn2hex(result) << " decimal variant: " << dec << std::endl;

            hex += bn2hex(result);
        }

        BN_free(r);
        BN_free(s);
        BN_free(gcd);
        BN_free(temp1);
        BN_free(temp2);
        BN_free(result);
        BN_CTX_free(ctx);
    }

    void RSA::decrypt_rsa(const BIGNUM* a, const BIGNUM* b, BIGNUM* x, BIGNUM* y, BN_CTX* ctx) {
        BIGNUM* q = BN_new();
        BIGNUM* r = BN_new();
        BIGNUM* x1 = BN_new();
        BIGNUM* y1 = BN_new();
        BIGNUM* temp = BN_new();

        if (BN_is_zero(b)) {
            BN_one(x);
            BN_zero(y);
            return;
        }

        BN_div(q, r, a, b, ctx);
        decrypt_rsa(b, r, x1, y1, ctx);

        BN_mul(temp, q, x1, ctx);
        BN_sub(x, y1, temp);
        BN_copy(y, x1);

        BN_free(q);
        BN_free(r);
        BN_free(x1);
        BN_free(y1);
        BN_free(temp);
    }

    std::string RSA::bn2hex(BIGNUM* bn) {
        char* hex_str = BN_bn2hex(bn);
        std::string hex_(hex_str);

        OPENSSL_free(hex_str);
        return hex_;
    }
}