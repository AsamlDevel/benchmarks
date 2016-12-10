#!/bin/bash


swig -python skpyext.i

gcc -fPIC -c skpyext.c skpyext_wrap.c -I/usr/include/python2.7

gcc -shared skpyext.o skpyext_wrap.o -o _skpyext.so

./multithreading_test.py

