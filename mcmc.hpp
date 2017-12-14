#ifndef MCMC_HPP_INCLUDED
#define MCMC_HPP_INCLUDED

#include <vector>
#include <ctime>
#include <random>
#include <climits>
#include "toolbox.hpp"
using namespace std; //To remove at the end

class MCMC{
public:
    MCMC(const vector<double>& s, const vector<pair<vector<double>, int> >& p,
         double b);
    MCMC(int dim, const vector<pair<vector<double>, int> >& p,
         double b, default_random_engine& g);
    void next_state(default_random_engine& g);
    void advance_state(int t, default_random_engine& g, int pace = INT_MAX, double delta = 0);
    const vector<double>& get_state();
    void error_rate(int& p, int& q);
private:
    int n;
    vector<double> state;
    vector<pair<vector<double>, int> > points;
    double beta;
};

#endif // MCMC_HPP_INCLUDED
