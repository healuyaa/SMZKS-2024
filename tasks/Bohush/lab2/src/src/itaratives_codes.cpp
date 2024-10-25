#include "iterative_codes.hpp"

#include <bitset>
#include <cstdint>
#include <iostream>
#include <memory>
#include <vector>

namespace code {
    Iteratives::Iteratives(int number, SIZES size, Paritets paritet) : number(number), v(std::make_unique<Data>()), size(size), paritet(paritet) {
        if(size == SIZES::size_square) {
            v->matrix.resize(SIZE_MATRIX_4);
            for(auto& m: v->matrix) {
                m.resize(SIZE_MATRIX_4);
            }

            v->paritet_x.resize(SIZE_MATRIX_4);
            v->paritet_y.resize(SIZE_MATRIX_4);

            IntToMatrix(number);
        } else if(size == SIZES::size_rectangle) {
            v->matrix.resize(SIZE_MATRIX_8);
            for(auto& m: v->matrix) {
                m.resize(SIZE_MATRIX_2);
            }

            v->paritet_x.resize(SIZE_MATRIX_8);
            v->paritet_y.resize(SIZE_MATRIX_2);

            IntToMatrix(number);
        }

    }

    void Iteratives::SetCode(int i, int j) {
        v->matrix[i][j] ^= 1;
    }

    void Iteratives::encodeSquare() {     
        int temp_xy = 0;

        for (int i = 0; i < SIZE_MATRIX_4; ++i) {
            int temp_x = 0;
            int temp_y = 0;

            for(int j = 0; j < SIZE_MATRIX_4; ++j) {
                v->matrix[i][j] == 1 ? ++temp_x : temp_x;
                v->matrix[j][i] == 1 ? ++temp_y : temp_y;

                temp_xy ^= v->matrix[i][j];
            }

            v->paritet_y[i] = (temp_x & 1) == 0 ? 0 : 1;
            v->paritet_x[i] = (temp_y & 1) == 0 ? 0 : 1;
        }

        int count = 0;
        for(int i = 0; i < SIZE_MATRIX_4; ++i) {
            (v->paritet_x[i] & 1) == 0 ? count : ++count;
            (v->paritet_y[i] & 1) == 0 ? count : ++count;    

            temp_xy ^= v->paritet_x[i] ^ v->paritet_y[i];
        }

        if(paritet == Paritets::three) {
            v->paritet_xy = temp_xy;
        }
    }

    void Iteratives::encodeRectangle() {
        int temp_xy = 0;

        for (int i = 0; i < SIZE_MATRIX_2; ++i) {
            int temp_x = 0;

            for (int j = 0; j < SIZE_MATRIX_8; ++j) {
                v->matrix[i][j] == 1 ? ++temp_x : temp_x;
                temp_xy ^= v->matrix[i][j];
            }

            v->paritet_y[i] = (temp_x & 1) == 0 ? 0 : 1;
        }

        for (int j = 0; j < SIZE_MATRIX_8; ++j) {
            int temp_y = 0;

            for (int i = 0; i < SIZE_MATRIX_2; ++i) {
                v->matrix[i][j] == 1 ? ++temp_y : temp_y;
            }

            v->paritet_x[j] = (temp_y & 1) == 0 ? 0 : 1;
        }

        int count = 0;
        for(int i = 0; i < SIZE_MATRIX_8; ++i) {
            (v->paritet_x[i] & 1) == 0 ? count : ++count;
            temp_xy ^= v->paritet_x[i];
        }
        for(int i = 0; i < SIZE_MATRIX_2; ++i) {
            (v->paritet_y[i] & 1) == 0 ? count : ++count;
            temp_xy ^= v->paritet_y[i];
        }

        if(paritet == Paritets::three) {
            v->paritet_xy = temp_xy;
        }
    }

    void Iteratives::decodeSquare() {
        bool errorFound = true;

        std::vector<int> temp_paritet_x(SIZE_MATRIX_4, 0);
        std::vector<int> temp_paritet_y(SIZE_MATRIX_4, 0);

        while (errorFound) {
            errorFound = false;
            int error_x = -1;
            int error_y = -1;

            int temp_xy = 0;

            for (int i = 0; i < SIZE_MATRIX_4; ++i) {
                int temp_x = 0;
                int temp_y = 0;                

                for (int j = 0; j < SIZE_MATRIX_4; ++j) {
                    v->matrix[i][j] == 1 ? ++temp_x : temp_x;
                    v->matrix[j][i] == 1 ? ++temp_y : temp_y;

                    temp_xy ^= v->matrix[i][j];
                }

                temp_x = (temp_x & 1) == 0 ? 0 : 1;
                temp_y = (temp_y & 1) == 0 ? 0 : 1;

                temp_paritet_x[i] = temp_y;
                temp_paritet_y[i] = temp_x;

                if (temp_x != v->paritet_y[i]) {
                    error_x = i;
                }
                if (temp_y != v->paritet_x[i]) {
                    error_y = i;
                }

                if(paritet == Paritets::three) {
                    int count = 0;

                    for(int i = 0; i < SIZE_MATRIX_4; ++i) {
                        (temp_paritet_x[i] & 1) == 0 ? count : ++count;
                        (temp_paritet_y[i] & 1) == 0 ? count : ++count;

                        temp_xy ^= temp_paritet_x[i] ^ temp_paritet_y[i];
                    }

                    int temp_compare = temp_xy;
                    
                    if(temp_compare != v->paritet_xy) {
                        std::cout << "Parity error detected!" << std::endl;
                        errorFound = true;
                    }
                }

                if (error_x != -1 && error_y != -1) {
                    std::cout << "Error pos: " << error_x << ' ' << error_y << std::endl;
                    SetCode(error_x, error_y);
                    errorFound = true;
                }
            }
        }

        std::cout << "No more errors" << std::endl;
    }

    void Iteratives::decodeRectangle() {
        bool errorFound = true;

        std::vector<int> temp_paritet_x(SIZE_MATRIX_8, 0);
        std::vector<int> temp_paritet_y(SIZE_MATRIX_2, 0);

        while (errorFound) {
            errorFound = false;

            int error_x = -1;
            int error_y = -1;

            int temp_xy = 0;

            int err_pref_x, err_pref_y;

            for (int i = 0; i < SIZE_MATRIX_2; ++i) {
                std::uint8_t temp_x = 0;

                for (int j = 0; j < SIZE_MATRIX_8; ++j) {
                    v->matrix[i][j] == 1 ? ++temp_x : temp_x;

                    temp_xy ^= v->matrix[i][j];
                }

                temp_x = (temp_x & 1) == 0 ? 0 : 1;

                temp_paritet_y[i] = temp_x;

                if (temp_x != v->paritet_y[i]) {
                    err_pref_x = i;
                    error_x = i;
                }
            }

            for (int j = 0; j < SIZE_MATRIX_8; ++j) {
                std::uint8_t temp_y = 0;

                for (int i = 0; i < SIZE_MATRIX_2; ++i) {
                    v->matrix[i][j] == 1 ? ++temp_y : temp_y;
                }

                temp_y = (temp_y & 1) == 0 ? 0 : 1;

                temp_paritet_x[j] = temp_y;

                if (temp_y != v->paritet_x[j]) {
                    err_pref_y = j;
                    error_y = j;
                }
            }

            if(paritet == Paritets::three) {
                std::uint8_t count = 0;

                for(auto temp: temp_paritet_y) {                
                    (temp & 1) == 0 ? count : ++count; 
                    temp_xy ^= temp;
                }

                for(auto temp : temp_paritet_x) {
                    (temp & 1) == 0 ? count : ++count;
                    temp_xy ^= temp;
                }

                std::uint8_t temp_compare = temp_xy;
                
                if(temp_compare != v->paritet_xy || error_x != -1 || error_y != -1) {
                    std::cout << "Parity error detected!" << std::endl;
                    errorFound = true;
                }
            }
            
            if (error_x != -1 && error_y != -1) {
                std::cout << "Error pos: " << error_x << ' ' << error_y << std::endl;
                SetCode(error_x, error_y);
                errorFound = true;
            } else if(error_x != -1 || error_y != -1) {
                std::cout << "Error pos: " << err_pref_x << ' ' << err_pref_y << std::endl;
                SetCode(err_pref_x, err_pref_y);
                errorFound = true;
            }
        }

        std::cout << "No more errors" << std::endl;
    }

    void Iteratives::printSquare() {
        for(int i = 0; i < SIZE_MATRIX_4; ++i) {
            for(int j = 0; j < SIZE_MATRIX_4; ++j) {
                std::cout << (int)v->matrix[i][j] << ' ';
            }
            std::cout << "  " << (int)v->paritet_y[i];
            std::cout << std::endl;
        }
        std::cout << std::endl;

        for(auto x: v->paritet_x) {
            std::cout << (int)x << ' ';
        }
        std::cout << "  " << (int)v->paritet_xy;
        std::cout << std::endl;
    }

    void Iteratives::printRectangle() {
        for(int i = 0; i < SIZE_MATRIX_2; ++i) {
            for(int j = 0; j < SIZE_MATRIX_8; ++j) {
                std::cout << (int)v->matrix[i][j] << ' ';
            }
            std::cout << "  " << (int)v->paritet_y[i];
            std::cout << std::endl;
        }
        std::cout << std::endl;

        for(auto x: v->paritet_x) {
            std::cout << (int)x << ' ';
        }
        std::cout << "  " << (int)v->paritet_xy;
        std::cout << std::endl;
    }

    void Iteratives::IntToMatrix(int number) {
        std::bitset<SIZE_BITS> binary(number);

        if(size == SIZES::size_square) {            
            for(int i = 0; i < SIZE_MATRIX_4; ++i) {
                for(int j = 0; j < SIZE_MATRIX_4; ++j) {
                    v->matrix[i][j] = binary[i * SIZE_MATRIX_4 + j];
                }
            }
        } else if(size == SIZES::size_rectangle) {
            for(int i = 0; i < SIZE_MATRIX_2; ++i) {
                for(int j = 0; j < SIZE_MATRIX_8; ++j) {
                    v->matrix[i][j] = binary[i * SIZE_MATRIX_8 + j];
                }
            }
        }
    }


    Multiple::Multiple(int number, LayersVariable variable, Paritets paritet) : number(number), variable(variable), paritet(paritet) {
        v.resize(SIZE_LAYERS);
        for(auto& v_ : v) {
            v_ = std::make_unique<DataM>();
        }

        for(auto& _v: v) {
            if(variable == LayersVariable::four_two) {
                _v->matrix.resize(SIZE_MATRIX_4);
                for(auto& m: _v->matrix) {
                    m.resize(SIZE_MATRIX_2);
                }

                _v->paritet_x.resize(SIZE_MATRIX_4);
                _v->paritet_y.resize(SIZE_MATRIX_2);

                if(paritet >= Paritets::four) {
                    _v->paritet_dl.resize(SIZE_MATRIX_4);
                    _v->paritet_dr.resize(SIZE_MATRIX_4);
                }

                if(paritet == Paritets::five) {                   
                    _v->paritets_z.resize(SIZE_MATRIX_4);
                    for(auto& z: _v->paritets_z) {
                        z.resize(SIZE_MATRIX_2);
                    }
                }

            } else if(variable == LayersVariable::two_four) {
                _v->matrix.resize(SIZE_MATRIX_2);
                for(auto& m: _v->matrix) {
                    m.resize(SIZE_MATRIX_4);
                }

                _v->paritet_x.resize(SIZE_MATRIX_2);
                _v->paritet_y.resize(SIZE_MATRIX_4);

                if(paritet >= Paritets::four) {
                    _v->paritet_dl.resize(SIZE_MATRIX_4);
                    _v->paritet_dr.resize(SIZE_MATRIX_4);
                }

                if(paritet == Paritets::five) {
                    _v->paritets_z.resize(SIZE_MATRIX_2);
                    for(auto& z: _v->paritets_z) {
                        z.resize(SIZE_MATRIX_4);
                    }
                }                
            }
        }

        IntToMatrix(number);
    }

    void Multiple::SetCode(int i, int j) {
        if (variable == LayersVariable::four_two) {
            if(j < SIZE_MATRIX_2) {
                v[0]->matrix[i][j] ^= 1;
            } else {
                v[1]->matrix[i][j - SIZE_MATRIX_2] ^= 1;
            }
        } else if(variable == LayersVariable::two_four) {
            if(i < SIZE_MATRIX_2) {
                v[0]->matrix[i][j] ^= 1;
            } else {
                v[1]->matrix[i - SIZE_MATRIX_2][j] ^= 1;
            }
        }
    }

    void Multiple::encodeMultiple() {
        if(variable == LayersVariable::four_two) {
            for(auto &v_: v) {
                int temp_xy = 0;
                
                for (int i = 0; i < SIZE_MATRIX_2; ++i) {
                    std::uint8_t temp_x = 0;

                    for (int j = 0; j < SIZE_MATRIX_4; ++j) {
                        temp_x ^= v_->matrix[j][i];
                        temp_xy ^= v_->matrix[j][i];
                    }

                    v_->paritet_y[i] = temp_x;
                }

                for (int j = 0; j < SIZE_MATRIX_4; ++j) {
                    uint8_t temp_y = 0;

                    for (int i = 0; i < SIZE_MATRIX_2; ++i) {
                        temp_y ^= v_->matrix[j][i];
                    }

                    v_->paritet_x[j] = temp_y;
                }

                std::uint8_t count = 0;
                for(int i = 0; i < SIZE_MATRIX_4; ++i) {
                    count ^= v_->paritet_x[i];
                    temp_xy ^= v_->paritet_x[i];
                }
                for(int i = 0; i < SIZE_MATRIX_2; ++i) {
                    count ^= v_->paritet_y[i];
                    temp_xy ^= v_->paritet_y[i];
                }

                if(paritet >= Paritets::three) {
                    v_->paritet_xy = temp_xy;
                }

                if(paritet >= Paritets::four) {                
                    v_->paritet_dl[0] = v_->matrix[0][0] ^ v_->matrix[3][1];
                    v_->paritet_dl[1] = v_->matrix[1][0] ^ v_->matrix[0][1];
                    v_->paritet_dl[2] = v_->matrix[2][0] ^ v_->matrix[1][1];
                    v_->paritet_dl[3] = v_->matrix[3][0] ^ v_->matrix[2][1];

                    v_->paritet_dr[0] = v_->matrix[3][0] ^ v_->matrix[0][1];
                    v_->paritet_dr[1] = v_->matrix[2][0] ^ v_->matrix[3][1];
                    v_->paritet_dr[2] = v_->matrix[1][0] ^ v_->matrix[2][1];
                    v_->paritet_dr[3] = v_->matrix[0][0] ^ v_->matrix[1][1];
                }

                if(paritet == Paritets::five) {
                    for(int i = 0; i < SIZE_MATRIX_4; ++i) {
                        for(int j = 0; j < SIZE_MATRIX_2; ++j) {                        
                            v_->paritets_z[i][j] = v[0]->matrix[i][j] ^ v[1]->matrix[i][j];                            
                        }
                    }
                }
            }

        } else {
            for(auto &v_: v) {
                for (int i = 0; i < SIZE_MATRIX_4; ++i) {
                    int temp_x = 0;

                    for (int j = 0; j < SIZE_MATRIX_2; ++j) {
                        v_->matrix[i][j] == 1 ? ++temp_x : temp_x;
                    }

                    v_->paritet_y[i] = (temp_x & 1) == 0 ? 0 : 1;
                }

                for (int j = 0; j < SIZE_MATRIX_4; ++j) {
                    int temp_y = 0;

                    for (int i = 0; i < SIZE_MATRIX_2; ++i) {
                        v_->matrix[i][j] == 1 ? ++temp_y : temp_y;
                    }

                    v_->paritet_x[j] = (temp_y & 1) == 0 ? 0 : 1;
                }

                int count = 0;
                for(int i = 0; i < SIZE_MATRIX_4; ++i) {
                    (v_->paritet_x[i] & 1) == 0 ? count : ++count;
                }
                for(int i = 0; i < SIZE_MATRIX_2; ++i) {
                    (v_->paritet_y[i] & 1) == 0 ? count : ++count;
                }

                if(paritet >= Paritets::three) {
                    v_->paritet_xy = (count & 1) == 0 ? 0 : 1;
                }

                if(paritet >= Paritets::four) {                
                    v_->paritet_dl[0] = v_->matrix[0][0] ^ v_->matrix[3][1];
                    v_->paritet_dl[1] = v_->matrix[0][1] ^ v_->matrix[1][0];
                    v_->paritet_dl[2] = v_->matrix[0][2] ^ v_->matrix[1][1];
                    v_->paritet_dl[3] = v_->matrix[0][3] ^ v_->matrix[1][2];

                    v_->paritet_dr[0] = v_->matrix[0][3] ^ v_->matrix[1][0];
                    v_->paritet_dr[1] = v_->matrix[0][0] ^ v_->matrix[1][1];
                    v_->paritet_dr[2] = v_->matrix[0][1] ^ v_->matrix[1][2];
                    v_->paritet_dr[3] = v_->matrix[0][2] ^ v_->matrix[1][3];
                }

                if(paritet == Paritets::five) {
                    for(int i = 0; i < SIZE_MATRIX_4; ++i) {
                        for(int j = 0; j < SIZE_MATRIX_2; ++j) {                        
                            v_->paritets_z[i][j] = v[0]->matrix[i][j] ^ v[1]->matrix[i][j];
                        }
                    }                    
                }

            }

        }
    }

    void Multiple::decodeMultiple() {
        bool errorFound = true;

        std::vector<std::uint8_t> temp_paritet_x;
        std::vector<std::uint8_t> temp_paritet_y;

        std::vector<std::uint8_t> temp_paritet_dl;
        std::vector<std::uint8_t> temp_paritet_dr;

        std::vector<std::vector<std::uint8_t>> temp_paritet_z;

        if(paritet >= Paritets::three) {
            if(variable == LayersVariable::four_two) {
                temp_paritet_x.resize(SIZE_MATRIX_4, 0);
                temp_paritet_y.resize(SIZE_MATRIX_2, 0);

            } else {
                temp_paritet_x.resize(SIZE_MATRIX_2, 0);
                temp_paritet_y.resize(SIZE_MATRIX_4, 0);
            }
        }

        if(paritet >= Paritets::four) {
            temp_paritet_dl.resize(SIZE_MATRIX_4, 0);
            temp_paritet_dr.resize(SIZE_MATRIX_4, 0);
        }

        if(paritet == Paritets::five) {
            if(variable == LayersVariable::four_two) {
                temp_paritet_z.resize(SIZE_MATRIX_4);
                for(auto &z: temp_paritet_z) {
                    z.resize(SIZE_MATRIX_2, 0);
                }

            } else {
                temp_paritet_z.resize(SIZE_MATRIX_2);
                for(auto &z: temp_paritet_z) {
                    z.resize(SIZE_MATRIX_4, 0);
                }
            }
        }

        for(auto &v_: v) {
                do {
                    errorFound = false;

                    int error_x = -1;
                    int error_y = -1;

                    int error_xy = 0;

                    int error_x_dl = -1, error_y_dl = -1;
                    int error_x_dr = -1, error_y_dr = -1;

                    int error_zi = -1;
                    int error_zj = -1;

                    for (int i = 0; i < SIZE_MATRIX_2; ++i) {
                        int temp_x = 0;
                        for (int j = 0; j < SIZE_MATRIX_4; ++j) {
                            temp_x ^= v_->matrix[i][j];
                            error_xy ^= v_->matrix[i][j];
                        }
                        temp_paritet_y[i] = temp_x & 1;

                        if (temp_paritet_y[i] != v_->paritet_y[i]) {
                            error_x = i;
                        }
                    }

                    for (int j = 0; j < SIZE_MATRIX_4; ++j) {
                        int temp_y = 0;
                        for (int i = 0; i < SIZE_MATRIX_2; ++i) {
                            temp_y ^= v_->matrix[i][j];
                        }
                        temp_paritet_x[j] = temp_y & 1;

                        if (temp_paritet_x[j] != v_->paritet_x[j]) {
                            error_y = j;
                        }
                    }

                    if (paritet >= Paritets::four) {
                        temp_paritet_dl[0] = v_->matrix[0][0] ^ v_->matrix[3][1];
                        temp_paritet_dl[1] = v_->matrix[1][0] ^ v_->matrix[0][1];
                        temp_paritet_dl[2] = v_->matrix[2][0] ^ v_->matrix[1][1];
                        temp_paritet_dl[3] = v_->matrix[3][0] ^ v_->matrix[2][1];

                        temp_paritet_dr[0] = v_->matrix[3][0] ^ v_->matrix[0][1];
                        temp_paritet_dr[1] = v_->matrix[2][0] ^ v_->matrix[3][1];
                        temp_paritet_dr[2] = v_->matrix[1][0] ^ v_->matrix[2][1];
                        temp_paritet_dr[3] = v_->matrix[0][0] ^ v_->matrix[1][1];

                        for (int i = 0; i < SIZE_MATRIX_4; ++i) {
                            if (temp_paritet_dl[i] != v_->paritet_dl[i]) {
                                error_x_dl = i;
                            }
                            if (temp_paritet_dr[i] != v_->paritet_dr[i]) {
                                error_x_dr = i;
                            }
                        }

                        if (error_x_dl != -1 && error_x_dr != -1) {
                            error_y_dl = 3 - error_x_dl;
                            error_y_dr = 3 - error_x_dr;

                            if (error_y_dl == error_x_dr || error_y_dr == error_x_dl) {
                                // std::cout << "err pos dl dr" << std::endl;
                                errorFound = true;
                            }
                        }
                    }

                    if (paritet == Paritets::five) {
                        for (int i = 0; i < SIZE_MATRIX_4; ++i) {
                            for (int j = 0; j < SIZE_MATRIX_2; ++j) {
                                temp_paritet_z[i][j] = v[0]->matrix[i][j] ^ v[1]->matrix[i][j];

                                if (temp_paritet_z[i][j] != v_->paritets_z[i][j]) {
                                    error_zi = i;
                                    error_zj = j;
                                    errorFound = true;
                                }
                            }
                        }

                        if (error_zi != -1 && error_zj != -1) {
                            std::cout << "err pos z: " << error_zi << ", " << error_zj << std::endl;
                            SetCode(error_zi, error_zj);
                            errorFound = true;
                        }
                    }

                    // if (error_x != -1 && error_y != -1) {
                    //     std::cout << "Error pos: " << error_x << ' ' << error_y << std::endl;
                    //     SetCode(error_x, error_y);
                    //     errorFound = true;
                    // }

                } while (errorFound);

                std::cout << "No more errors" << std::endl;
            }

    }

    void Multiple::printMultiple() {
        for(auto &v_: v) {
            
            std::cout << "matrix: " <<  std::endl;
            for(int i = 0; i < SIZE_MATRIX_4; ++i) {
                for(int j = 0; j < SIZE_MATRIX_2; ++j) {
                    std::cout << (int)v_->matrix[i][j] << ' ';
                }
                std::cout << "  " << (int)v_->paritet_x[i];
                std::cout << std::endl;
            }
            std::cout << std::endl;
            for(auto y: v_->paritet_y) {
                std::cout << (int)y << ' ';
            }
            std::cout << "  " << (int)v_->paritet_xy;
            std::cout << std::endl;
            std::cout << std::endl;

            std::cout << "dl: " << std::endl;
            for(auto dl_: v_->paritet_dl)  {
                std::cout << (int)dl_ << ' ';
            }
            std::cout << std::endl;
            std::cout << std::endl;

            std::cout << "dr: " << std::endl;
            for(auto dr_: v_->paritet_dr)  {
                std::cout << (int)dr_ << ' ';
            }
            std::cout << std::endl;
            std::cout << std::endl;

            std::cout << "matrix z: " << std::endl;
            for(auto &z0: v_->paritets_z) {
                for(auto z1: z0) {
                    std::cout << (int)z1 << ' ';
                }
                std::cout << std::endl;
            }
            std::cout << std::endl;
        }
        std::cout << std::endl;
    }

    void Multiple::IntToMatrix(int number) {
        std::bitset<SIZE_BITS> binary(number);

        if (variable == LayersVariable::four_two) {
            for (int i = 0; i < SIZE_MATRIX_4; ++i) {
                for (int j = 0; j < SIZE_MATRIX_2; ++j) {
                    v[0]->matrix[i][j] = binary[i * SIZE_MATRIX_4 + j];
                    v[1]->matrix[i][j] = binary[i * SIZE_MATRIX_4 + j + SIZE_MATRIX_2];
                }
            }
        } else if (variable == LayersVariable::two_four) {
            for (int i = 0; i < SIZE_MATRIX_2; ++i) {
                for (int j = 0; j < SIZE_MATRIX_4; ++j) {
                    v[0]->matrix[i][j] = binary[i * SIZE_MATRIX_4 + j];
                    v[1]->matrix[i][j] = binary[(i + SIZE_MATRIX_2) * SIZE_MATRIX_4 + j];
                }
            }
        }
    }
}