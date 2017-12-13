#ifndef MCMC_HPP_INCLUDED
#define MCMC_HPP_INCLUDED

#include <vector>
#include <ctime>
#include <random>
using namespace std; //To remove at the end

class MCMC{
public:
    MCMC(vector<double>& s, vector<pair<vector<double>, int> >& p,
         double b);
    MCMC(int dim, vector<pair<vector<double>, int> >& p,
         double b, default_random_engine& g);
    void next_state(default_random_engine& g);
    void advance_state(int t, default_random_engine& g);
    const vector<double>& get_state();
    void error_rate(int& p, int& q);
private:
    int n;
    vector<double> state;
    vector<pair<vector<double>, int> > points;
    double beta;
};

#endif // MCMC_HPP_INCLUDED
