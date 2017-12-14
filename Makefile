PROG		= main
PRODNAME	= poulpe
CXX			= g++
CXXFLAGS	= -Wall -O3 -std=c++11
LIBRARY		= toolbox mcmc instance

OBJECTS		= $(LIBRARY:=.o)

default : $(OBJECTS)
	$(CXX) $(LDFLAGS) $(CXXFLAGS) $(STD) -o $(PRODNAME) $(PROG:=.cpp) $^
	
main.o : main.cpp mcmc.hpp instance.hpp
	$(CXX) -c $(CXXFLAGS) $(STD) $< -o $@
	
toolbox.o : toolbox.cpp toolbox.hpp
	$(CXX) -c $(CXXFLAGS) $(STD) $< -o $@
	
mcmc.o : mcmc.cpp mcmc.hpp toolbox.hpp
	$(CXX) -c $(CXXFLAGS) $(STD) $< -o $@
	
instance.o : instance.cpp instance.hpp toolbox.hpp
	$(CXX) -c $(CXXFLAGS) $(STD) $< -o $@
	
cleanall : clean
	rm -f $(PRODNAME)

clean :
	rm -f $(OBJECTS) $(PROG:=.o)