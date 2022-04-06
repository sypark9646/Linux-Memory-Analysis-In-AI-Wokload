# Linux-Trace-Analysis-In-AI-Wokload
- Extract traces of memory data when cache missed
- Analyze traces and find out how the analysis results should be reflected in system design. 
- Use [Valgrind](https://valgrind.org/) tool for analyze traces.


## Raw Trace Data
```txt
==190689== Callgrind, a call-graph generating cache profiler
==190689== Copyright (C) 2002-2017, and GNU GPL'd, by Josef Weidendorfer et al.
==190689== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==190689== Command: python3 ann_python_churn_modelling.py
==190689== Parent PID: 187980
==190689== 
--190689-- warning: L3 cache found, using its data for the LL simulation.
==190689== For interactive control, run 'callgrind_control -h'.
readi 0x0000000004001100 3 1648526782.529065056
write 0x0000001ffefffe48 8 1648526782.529086545
readi 0x0000000004001df0 4 1648526782.529311824
write 0x0000001ffefffe38 8 1648526782.529319584
readi 0x0000000004001dff 2 1648526782.529323137
write 0x000000000402d5e0 8 1648526782.529329596
readd 0x000000000402de68 8 1648526782.529333045
readd 0x000000000402e000 8 1648526782.529336239
write 0x000000000402e9f8 8 1648526782.529339402
readi 0x0000000004001e3e 3 1648526782.529342472
readi 0x0000000004001e9f 4 1648526782.529398374
write 0x000000000402ea98 8 1648526782.529459678
write 0x000000000402ea48 8 1648526782.529468060
readd 0x000000000402de88 8 1648526782.529473302
readi 0x0000000004002070 3 1648526782.529591505
readi 0x0000000004002090 3 1648526782.529641571
readi 0x0000000004002210 3 1648526782.529687106
write 0x000000000402ec88 8 1648526782.529733835
readd 0x000000000402dec8 8 1648526782.529787922
write 0x000000000402ea38 8 1648526782.529795152
write 0x000000000402eac8 8 1648526782.529799663
readd 0x000000000402df08 8 1648526782.529803805
readd 0x000000000402df48 8 1648526782.529808930
```

* data type
  * readi: read instruction
  * readd: read data
  * write
* (virtual) address
* referenced address size
* timestamp(sec)

## Tools
- gnuplot
- python pandas, numpy, matplotlib
