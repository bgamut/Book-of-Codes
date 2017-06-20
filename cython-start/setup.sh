cython --embed -o main.c main.py
gcc -Os -I /usr/include/python2.7/ -o main main.c -lpython2.7 -lpthread -lm -lutil -ldl
