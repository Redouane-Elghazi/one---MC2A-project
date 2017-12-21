#include <iostream>
#include <random>
#include <fstream>
#include <cstring>
#include "instance.hpp"
#include "mcmc.hpp"
#include "toolbox.hpp"

using namespace std;

int main(int argc, char* argv[]){
    int n = 100, m = 500, T = 1000;
    int pace = T/100;
    double beta = 1., delta = 0.;

	ofstream out;
	ifstream in;
	int seed = 0;
	bool mode_all = false; //true for all, false for the last

    switch(argc){
	case 8:
		delta = atof(argv[7]);
	case 7:
		pace = atoi(argv[6]);
	case 6:
		beta = atof(argv[5]);
	case 5:
		T = atoi(argv[4]);
	/*case 6:
		m = atoi(argv[5]);
	case 5:
		n = atoi(argv[4]);
		mode_all = (strcmp("all",argv[3]) == 0);*/
		seed = atoi(argv[3]);
        in.open(argv[2], ios::in);
		out.open(argv[1], ios::out | ios::app);
		break;
	default:
		cout << "./poulpe file.out seed mode_all n m=500 T=1000 beta=1. pace=10 delta=0. file.in" << endl;
		return 1;
    }

    default_random_engine g;
    g.seed(seed);
    in >> m >> n;
    vector<pair<vector<double>, int> > points(m);
    for(int i = 0; i<m; ++i){
        for(int j = 0; j<n; ++j){
            double x;
            cin >> x;
            points[i].first.push_back(x);
        }
    }
    for(int i = 0; i<m; ++i){
        int x;
        cin >> x;
        points[i].second = x;
    }
    int mtest;
    cin >> mtest;
    vector<vector<double> > test(mtest);
    for(int i = 0; i<mtest; ++i){
        for(int j = 0; j<n; ++j){
            double x;
            cin >> x;
            test[i].push_back(x);
        }
    }
    //instance problem(n, m, g);
    instance problem(points);
    MCMC solve(out, mode_all, n, problem.get_points(), beta, g);

	/*vector<double> state(problem.get_model());
	for(auto& x:state)
		x = -x;
    MCMC solve(out, mode_all, state, problem.get_points(), beta);
*/
/*
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
*/
	if(mode_all){
		out << T << endl;
	}
    solve.advance_state(T, g, pace, delta);
/*
    cout << "found vector is:" << endl;
    for(double x:solve.get_state())
        cout << x << " ";
    cout << endl;
    solve.error_rate(p,q);
    cout << p << "/" << q << endl;

	if(mode_all == false){
		int p,q;
		solve.error_rate(p,q);
		out << (double)p/q << " " << inner_product(problem.get_model().begin(),problem.get_model().end(),solve.get_state().begin(),0.)/n << endl;
	}
*/

    for(double x:solve.get_state())
        out << x << endl;
    out << endl;

    int p,q;
    solve.error_rate(p,q);
    out << 2.*p/q << endl;

    for(int i = 0; i<m; ++i){
        out << sgn(inner_product(test[i].begin(), test[i].end(),
                                 solve.get_state().begin(), 0.)) << endl;
    }
    out.close();
	return 0;
}
