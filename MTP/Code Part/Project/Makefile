LINKS = -lgmpxx -lgmp
COMP = g++ -Wall -std=c++17 -O3 -o
OBJ = g++ -Wall -std=c++17 -O3 -c


defaults: qsmain

qsmain: QS.o utility.o
	$(COMP) qsmain QS.o utility.o $(LINKS)

%.o: %.cpp
	$(OBJ) $<

utility.o: utility.cpp utility.h wrappers.h

clean:
	rm -rf *.o
