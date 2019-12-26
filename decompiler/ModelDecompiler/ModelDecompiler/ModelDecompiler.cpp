// ModelDecompiler.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "tf2_decomp.hpp"

int main(int count, char** args)
{
    if (count != 1) {
        printf("Wrong argument count");
        return -10000;
    }

    int result = 0;
    tf2decomp::Model model = tf2decomp::convertFromFile("barrel_water_blue.mdl", &result);
    return result;
}
