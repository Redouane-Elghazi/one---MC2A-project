#include <iostream>
#include <random>
#include <fstream>
#include <cstring>
#include "instance.hpp"
#include "mcmc.hpp"

using namespace std;

int main(int argc, char* argv[]){
    int n = 100, m = 500, T = 1000;
    int pace = T/100;
    double beta = 1., delta = 0.;

	ofstream out;
	int seed = 0;
	bool mode_all = false; //true for all, false for the last

    switch(argc){
	case 10:
		delta = atof(argv[9]);
	case 9:
		pace = atoi(argv[8]);
	case 8:
		beta = atof(argv[7]);
	case 7:
		T = atoi(argv[6]);
	case 6:
		m = atoi(argv[5]);
	case 5:
		n = atoi(argv[4]);
		mode_all = (strcmp("all",argv[3]) == 0);
		seed = atoi(argv[2]);
		out.open(argv[1], ios::out | ios::app);
		break;
	default:
		cout << "./poulpe file.out seed mode_all n m=500 T=1000 beta=1. pace=10 delta=0." << endl;
		return 1;
    }

    default_random_engine g;
    g.seed(seed);
    instance problem(n, m, g);
    MCMC solve(out, mode_all, n, problem.get_points(), beta, g);

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

	if(mode_all){
		out << T << endl;
	}
    solve.advance_state(T, g, pace, delta);
    cout << "found vector is:" << endl;
    for(double x:solve.get_state())
        cout << x << " ";
    cout << endl;
    solve.error_rate(p,q);
    cout << p << "/" << q << endl;

	if(mode_all == false){
			out << p << " " << inner_product(problem.get_model().begin(),problem.get_model().end(),solve.get_state().begin(),0) << endl;
	}
    out.close();
	return 0;
}
