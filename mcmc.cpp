#include <iostream>
#include "mcmc.hpp"
using namespace std;

int sgn(double x){
    if(x==0)
        return 0;
    else if(x<0)
        return -1;
    else
        return 1;
}

MCMC::MCMC(vector<double>& s, vector<pair<vector<double>, int> >& p,
           double b): state(s), points(p), beta(b){
    n = state.size();
}

MCMC::MCMC(int dim, vector<pair<vector<double>, int> >& p, double b,
           default_random_engine& g): n(dim), points(p), beta(b){
    state = vector<double>(n,0);
    uniform_int_distribution<int> b_unif(0,1);
    for(int i = 0; i<n; ++i)
        state[i] = 2*b_unif(g)-1;
}

void MCMC::next_state(default_random_engine& g){
    uniform_real_distribution<double> r_unif(0,1);
    uniform_int_distribution<int> i_unif(0,n-1);
    double coin = r_unif(g);
    int i = i_unif(g);
    double E1 = 0, E2 = 0;
    double label;
    for(auto& point:points){
        label = inner_product(state.begin(), state.end(),
                              point.first.begin(), 0.);
        E1+=(point.second-sgn(label))*(point.second-sgn(label));
        label = label - 2*state[i]*point.first[i];
        E2+=(point.second-sgn(label))*(point.second-sgn(label));
    }
    E1 = E1/2;
    E2 = E2/2;
    double p = min(1., exp(-beta*(E2-E1)));
    if(coin<=p)
        state[i]=-state[i];
}

void MCMC::advance_state(int t, default_random_engine& g){
    int p,q;
    error_rate(p,q);
    for(int i = 0; i<t and p!=0; ++i){
        next_state(g);
        error_rate(p,q);
    }
}

const vector<double>& MCMC::get_state(){
    return state;
}

void MCMC::error_rate(int& p, int& q){
    q = points.size();
    p = 0;
    double label;
    for(auto& point:points){
        label = inner_product(state.begin(), state.end(),
                              point.first.begin(), 0.);
        if(sgn(label) != point.second)
            ++p;
    }
}

int main(){
    int n = 100, m = 1000;
    double beta = 1;
    default_random_engine g;
    g.seed(0);
    vector<pair<vector<double>, int> > points;
    vector<double> real_model(n), start(n);
    uniform_int_distribution<int> b_unif(0, 1);
    for(int i = 0; i<n; ++i){
        real_model[i] = 2*b_unif(g)-1;
        start[i] = -real_model[i];
    }
    normal_distribution<double> norm(0, 1);
    for(int j = 0; j<m; ++j){
        vector<double> p(n);
        for(int i = 0; i<n; ++i){
            p[i] = norm(g);
        }
        double label = inner_product(real_model.begin(), real_model.end(),
                                     p.begin(), 0.);
        points.emplace_back(p, sgn(label));
    }
    MCMC test(n, points, beta, g);
//    MCMC test(start, points, beta);
    cout << "original is:" << endl;
    for(double x:real_model)
        cout << x << " ";
    cout << endl;
    int p,q;
    cout << "starting vector is:" << endl;
    for(double x:test.get_state())
        cout << x << " ";
    cout << endl;
    test.error_rate(p,q);
    cout << p << "/" << q << endl;

    test.advance_state(1000, g);
    cout << "found vector is:" << endl;
    for(double x:test.get_state())
        cout << x << " ";
    cout << endl;
    test.error_rate(p,q);
    cout << p << "/" << q << endl;
    return 0;
}
