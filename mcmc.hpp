#ifndef MCMC_HPP_INCLUDED
#define MCMC_HPP_INCLUDED

#include <vector>
#include <ctime>
#include <random>
#include <climits>
#include <fstream>
#include "toolbox.hpp"
using namespace std; //To remove at the end

class MCMC{
public:
    MCMC(ofstream& f, bool mode, const vector<double>& s, const vector<pair<vector<double>, int> >& p,
         double b);
    MCMC(ofstream& f, bool mode, int dim, const vector<pair<vector<double>, int> >& p,
         double b, default_random_engine& g);
    double next_state(default_random_engine& g);
    void advance_state(int t, default_random_engine& g, int pace = INT_MAX, double delta = 0);
    const vector<double>& get_state();
    void error_rate(int& p, int& q);
private:
    ofstream& out;
    bool mode_all;
    int n;
    vector<double> state;
    vector<pair<vector<double>, int> > points;
    double beta;
};

#endif // MCMC_HPP_INCLUDED
