#include <iostream>
#include <random>
#include "instance.hpp"
#include "mcmc.hpp"
using namespace std;

int main(int argc, char* argv[]){
    int n = 100, m = 500, T = 1000;
    int pace = T/100;
    double beta = 0, delta = 0.01;

    switch(argc){
	case 7:
		delta = atof(argv[6]);
	case 6:
		pace = atoi(argv[5]);
	case 5:
		beta = atof(argv[4]);
	case 4:
		T = atoi(argv[3]);
	case 3:
		m = atoi(argv[2]);
	case 2:
		n = atoi(argv[1]);
    }

    default_random_engine g;
    g.seed('E'*'n'*'g'*'u'+'e'*'r'*'r'*'a'+'n'*'d');
    instance problem(n, m, g);
    MCMC solve(n, problem.get_points(), beta, g);

    cout << "original is:" << endl;
    for(double x:problem.get_model())
        cout << x << " ";
    cout << endl;

    int p,q;
    cout << "starting vector is:" << endl;
    for(double x:solve.get_state())
        cout << x << " ";
    cout << endl;
    solve.error_rate(p,q);
    cout << p << "/" << q << endl;

    solve.advance_state(T, g, pace, delta);
    cout << "found vector is:" << endl;
    for(double x:solve.get_state())
        cout << x << " ";
    cout << endl;
    solve.error_rate(p,q);
    cout << p << "/" << q << endl;
	return 0;
}
