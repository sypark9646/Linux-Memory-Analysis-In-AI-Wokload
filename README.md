# Linux-Trace-Analysis-In-AI-Wokload
- Extract traces of memory data when cache missed
- Analyze traces and find out how the analysis results should be reflected in system design. 
- Use [Valgrind](https://valgrind.org/) tool for analyze traces.


## Raw Trace Data
```text
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

## Check
#### /proc/{PID}/maps
- 모든 프로세스는 가상 메모리 매니저에 의해 제공되는 가장 주소공간을 가지는데, 이러한 프로세스의 메모리 주소 공간을 보여준다.
- address, permission, offset, device number(major:minor), inode, pathname 순서로 표기된다.
  - permission
  - permission에서 p=private(copy on write)
- `code segment`; r-xp, 실행할 수 있는 코드가 저장된 메모리 공간은 읽고 실행할 수 있는 권한은 필요하나, 쓰기 권한은 필요없음
- `data segment`; rw-p, data 영역은 읽고 쓸수는 있지만, 실행할 수 있는 영역은 아니다. Data segments에 위치하는 변수들은 초기화된 전역변수들이다.
  ```text
  00400000-00423000 r--p 00000000 08:05 4588536                            /usr/bin/python3.8
  00423000-006b8000 r-xp 00023000 08:05 4588536                            /usr/bin/python3.8
  006b8000-008f5000 r--p 002b8000 08:05 4588536                            /usr/bin/python3.8
  008f5000-008f6000 r--p 004f4000 08:05 4588536                            /usr/bin/python3.8
  008f6000-0093d000 rw-p 004f5000 08:05 4588536                            /usr/bin/python3.8
  ```
- `shared library`; 실행파일의 공유 라이브러리가 로드되는 위치를 정의한다.
  ```text
  04000000-04001000 r--p 00000000 08:05 4589712                            /usr/lib/x86_64-linux-gnu/ld-2.31.so
  04001000-04024000 r-xp 00001000 08:05 4589712                            /usr/lib/x86_64-linux-gnu/ld-2.31.so
  04024000-0402c000 r--p 00024000 08:05 4589712                            /usr/lib/x86_64-linux-gnu/ld-2.31.so
  0402d000-0402e000 r--p 0002c000 08:05 4589712                            /usr/lib/x86_64-linux-gnu/ld-2.31.so
  0402e000-0402f000 rw-p 0002d000 08:05 4589712                            /usr/lib/x86_64-linux-gnu/ld-2.31.so
  ```
- `heap segment`; Heap 변수(런타임에 동적 할당)들이 위치한다. r추가로 Heap segment에는 bss section도 포함되어 있다. 
  - bss section: 초기화되지 않은 전역변수들이 위치하는 메모리 영역
- `stack segment`; 지역 변수들이나 함수 파라미터등 다양한 요소들이 위치한다.
  ```text
  7ffcf0630000-7ffcf0651000 rw-p 00000000 00:00 0                          [stack]
  7ffcf079f000-7ffcf07a3000 r--p 00000000 00:00 0                          [vvar]
  ffffffffff600000-ffffffffff601000 --xp 00000000 00:00 0                  [vsyscall]
  ```
- 출처: https://linuxias.github.io/linux/debugging/proc_filesystem/
- 출처: https://www.baeldung.com/linux/proc-id-maps
#### pmap -x {PID} | less
#### /proc/{PID}/status
```text
Name:	callgrind-amd64
Umask:	0002
State:	R (running)
...
VmPeak:	 1840320 kB
VmSize:	 1840320 kB
VmLck:	       0 kB
...
VmData:	  484604 kB
VmStk:	     132 kB
VmExe:	    1912 kB
VmLib:	 1311712 kB
VmPTE:	    1156 kB
VmSwap:	       0 kB
...
```
- `VmSize`: 프로세스에 할당된 SWAP 메모리 + 물리 메모리의 합산량
  - `SWAP 사용량`=`VmSize`-`VmRSS`
- `VmRSS`: 프로세스에 실제 할당된 물리적 메모리 사이즈
- `VmLck`: 가상메모리에 스왑아웃 될수 없는 영역에 대한 메모리의 크기
- `VmData`: 프로세스를 실행하기위한 동적 Heap 영역
- `VmStk`: 프로세스 내에서 수행되는 지역변수 할당을 위한 Stack 영역
- `VmExe`: 프로세스의 실행코드 영역 (전역변수 및 실행코드)
- `VmLib`: 동적으로 연결된 라이브러리 영역
## Tools
- gnuplot
- python pandas, numpy, matplotlib
