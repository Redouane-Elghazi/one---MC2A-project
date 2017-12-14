#include <iostream>
#include "instance.hpp"
using namespace std;

instance::instance(int dim, int sample, default_random_engine& g){
    n = dim;
    m = sample;
    uniform_int_distribution<int> b_unif(0, 1);
    for(int i = 0; i<n; ++i){
        model.push_back(2*b_unif(g)-1);
    }
    normal_distribution<double> norm(0, 1);
    for(int j = 0; j<m; ++j){
        vector<double> p(n);
        for(int i = 0; i<n; ++i){
            p[i] = norm(g);
        }
        double label = inner_product(model.begin(), model.end(),
                                     p.begin(), 0.);
        points.emplace_back(p, sgn(label));
    }
}

instance::instance(vector<double> real_model, int sample, default_random_engine& g){
    n = real_model.size();
    m = sample;
    model = real_model;
    normal_distribution<double> norm(0, 1);
    for(int j = 0; j<m; ++j){
        vector<double> p(n);
        for(int i = 0; i<n; ++i){
            p[i] = norm(g);
        }
        double label = inner_product(model.begin(), model.end(),
                                     p.begin(), 0.);
        points.emplace_back(p, sgn(label));
    }
}

const vector<double>& instance::get_model(){
    return model;
}

const vector<pair<vector<double>, int> >& instance::get_points(){
    return points;
}
