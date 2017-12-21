#include <iostream>
#include "toolbox.hpp"
using namespace std;

int sgn(double x){
    if(x<0)
        return -1;
    else if(x>0)
        return 1;
    else{
        exit(1);
        return 0;
    }
}
