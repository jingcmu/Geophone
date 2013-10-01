#!/bin/sh

mkdir build
cd build
`which cmake` ..

make

cp libGeophone.so ../Geophone.so
