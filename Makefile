PROG		= mcmc
PRODNAME	= poulpe
CXX			= g++
CXXFLAGS	= -Wall -O3 -std=c++11
LIBRARY		= mcmc

OBJECTS		= $(LIBRARY:=.o) $(PROG:=.o)

default : $(OBJECTS)
	$(CXX) $(LDFLAGS) $(CXXFLAGS) $(STD) -o $(PRODNAME) $^
	
	
cleanall : clean
	rm -f $(PRODNAME)

clean :
	rm -f $(OBJECTS) $(PROG:=.o)