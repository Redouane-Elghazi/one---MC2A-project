#include <iostream>
#include "mcmc.hpp"
using namespace std;

MCMC::MCMC(const vector<double>& s, const vector<pair<vector<double>, int> >& p,
           double b): state(s), points(p), beta(b){
    n = state.size();
}

MCMC::MCMC(int dim, const vector<pair<vector<double>, int> >& p, double b,
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

/*void MCMC::advance_state(int t, default_random_engine& g){
    int p,q;
    for(int i = 0; i<t; ++i){
        if(i%(t/100)==0){
            error_rate(p,q);
            cerr << i/(t/100) << "% of the execution: " ;
            cerr << 100.*p/q << "% error rate" << endl;
            if(p==0)
                break;
        }
        next_state(g);
    }
}*/

void MCMC::advance_state(int t, default_random_engine& g, int pace, double delta){
    int p,q;
    for(int i = 0; i<t; ++i){
        if(i%(t/100)==0){
            error_rate(p,q);
            cerr << i/(t/100) << "% of the execution: " ;
            cerr << 100.*p/q << "% error rate" << endl;
            if(p==0)
                break;
        }
        next_state(g);
        if((i+1)%pace == 0)
            beta += delta;
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
