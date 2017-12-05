PROG		= main
PRODNAME	= mcmc
CXX			= g++
CXXFLAGS	= -Wall -O3 -std=c++11
LIBRARY		= model

OBJECTS		= $(LIBRARY:=.o) $(PROG:=.o)

default : $(OBJECTS)
	$(CXX) $(LDFLAGS) $(CXXFLAGS) $(STD) -o $(PRODNAME) $^
	
	
cleanall : clean
	rm -f $(PRODNAME) $(TASKCREATORS)

clean :
	rm -f $(OBJECTS) $(PROG:=.o) $(TASKCREATORS:=.o)