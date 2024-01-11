cd src || exit 1

if [[ $1 == test ]]
then
  make tests && ./tests
elif [[ $1  == run ]]
then
  make && ./qsmain --level 4
elif [[ $1 == clean ]]
then
  make clean && make
elif [[ -z "$1" ]]
then
  make
else
  printf "invalid argument\n" 
fi