#!/bin/sh

gnuplot -p -e "set datafile separator ','; \
	set style fill solid border; \
	set style circle radius 0.01; \
	set output '/home/soyeon/logicalTime_blockAddress.png'; \
	plot '/home/soyeon/memdf.csv' using 0:4;"
