#include "RSA-hack.hpp"

#include <iostream>

namespace RSA_h {
    Tools::Tools(std::string N, std::string e, std::vector<std::string> blocks) {
        this->N = BN_new();
        this->e = BN_new();

        BN_dec2bn(&this->N, N.c_str());
        BN_dec2bn(&this->e, e.c_str());

        encrypted_blocks.resize(13);
        for(auto &eb: encrypted_blocks) {
            eb = BN_new();
        }

        for(int i = 0; i < blocks.size(); ++i) {
            BN_dec2bn(&encrypted_blocks[i], blocks[i].c_str());
        }
    }

    Tools::~Tools() {
        BN_free(N);
        BN_free(e);

        for (auto& block : encrypted_blocks) {
            BN_free(block);
        }
    }

    void Tools::BN_sqrt_manual(BIGNUM* result, const BIGNUM* N, BN_CTX* ctx) {
        BIGNUM* low = BN_new();
        BIGNUM* high = BN_new();
        BIGNUM* mid = BN_new();
        BIGNUM* mid_squared = BN_new();

        BN_one(low);
        BN_copy(high, N);

        while (BN_cmp(low, high) <= 0) {
            BN_add(mid, low, high);
            BN_rshift1(mid, mid);

            BN_sqr(mid_squared, mid, ctx);

            int cmp = BN_cmp(mid_squared, N);
            if (cmp == 0) {
                BN_copy(result, mid);
                break;
            } else if (cmp < 0) {
                BN_copy(low, mid);
                BN_add(low, low, BN_value_one());
            } else {
                BN_copy(high, mid);
                BN_sub(high, high, BN_value_one());
            }
        }

        BN_copy(result, low);

        BN_free(low);
        BN_free(high);
        BN_free(mid);
        BN_free(mid_squared);
    }

    void Tools::factorize_N(const BIGNUM* N, BIGNUM*& p, BIGNUM*& q) {
        BN_CTX* ctx = BN_CTX_new();
        BIGNUM* t = BN_new();
        BIGNUM* S = BN_new();
        BIGNUM* check = BN_new();

        BN_sqrt_manual(t, N, ctx);

        while (true) {
            BIGNUM* t_squared = BN_new();
            BIGNUM* difference = BN_new();
            BN_sqr(t_squared, t, ctx);
            BN_sub(difference, t_squared, N);

            BN_sqrt_manual(S, difference, ctx);
            BN_sqr(check, S, ctx);
            if (BN_cmp(check, difference) == 0) {
                BIGNUM* temp_p = BN_new();
                BIGNUM* temp_q = BN_new();

                BN_add(temp_p, t, S);
                BN_sub(temp_q, t, S);

                BN_copy(p, temp_p);
                BN_copy(q, temp_q);
                BN_free(temp_p);
                BN_free(temp_q);
                break;
            }

            BN_add(t, t, BN_value_one());
            BN_free(t_squared);
            BN_free(difference);
        }

        BN_free(t);
        BN_free(S);
        BN_free(check);
        BN_CTX_free(ctx);
    }

    void Tools::decrypt_rsa() {
        BIGNUM* p = BN_new();
        BIGNUM* q = BN_new();
        factorize_N(N, p, q);

        BIGNUM* phi = BN_new();
        BIGNUM* one = BN_new();
        BN_one(one);
        
        BIGNUM* p_minus_1 = BN_new();
        BIGNUM* q_minus_1 = BN_new();
        BN_sub(p_minus_1, p, one);
        BN_sub(q_minus_1, q, one);
        
        BN_CTX* ctx = BN_CTX_new();
        BN_mul(phi, p_minus_1, q_minus_1, ctx);

        BIGNUM* d = BN_new();
        BN_mod_inverse(d, e, phi, ctx);

        for (auto& C : encrypted_blocks) {
            BIGNUM* M = BN_new();
            BN_mod_exp(M, C, d, N, ctx);

            char* decrypted_message = BN_bn2hex(M);
            std::cout << "Decrypted message: " << decrypted_message << std::endl;

            hex += decrypted_message;

            OPENSSL_free(decrypted_message);
            BN_free(M);
        }

        BN_free(p);
        BN_free(q);
        BN_free(phi);
        BN_free(d);
        BN_free(one);
        BN_free(p_minus_1);
        BN_free(q_minus_1);
        BN_CTX_free(ctx);
    }

    std::string Tools::hex_to_utf8() {
        system("chcp 1251");

        std::string utf8;
        for (size_t i = 0; i < hex.length(); i += 2) {
            std::string byte = hex.substr(i, 2);
            char chr = (char)(int)strtol(byte.c_str(), nullptr, 16);
            utf8.push_back(chr);
        }
        return utf8;
    }

    void Tools::print() {
        std::string utf8_msg = hex_to_utf8();
        std::cout << "Decrypted UTF-8 message: " << utf8_msg << std::endl;
    }
}