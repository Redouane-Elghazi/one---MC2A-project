#ifndef INSTANCE_HPP_INCLUDED
#define INSTANCE_HPP_INCLUDED

#include <random>
#include <vector>
#include "toolbox.hpp"
using namespace std;

class instance{
public:
    instance(int dim, int sample, default_random_engine& g);
    instance(vector<double> real_model, int sample, default_random_engine& g);
    instance(vector<pair<vector<double>, int> > p);
    const vector<double>& get_model();
    const vector<pair<vector<double>, int> >& get_points();
private:
    int n;
    int m;
    vector<double> model;
    vector<pair<vector<double>, int> > points;
};

#endif // INSTANCE_HPP_INCLUDED
