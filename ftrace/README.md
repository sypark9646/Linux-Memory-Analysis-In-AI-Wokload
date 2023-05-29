# ftrace

- `./ftrace_command.sh [command]`: [COMMAND]에 해당하는 pid의 ftrace 추출
- 결과 파일 위치: `/sys/kernel/debug/tracing/trace`

```text
# tracer: function
#
# entries-in-buffer/entries-written: 1117450/14172603920   #P:20
#
#                                _-----=> irqs-off/BH-disabled
#                               / _----=> need-resched
#                              | / _---=> hardirq/softirq
#                              || / _--=> preempt-depth
#                              ||| / _-=> migrate-disable
#                              |||| /     delay
#           TASK-PID     CPU#  |||||  TIMESTAMP  FUNCTION
#              | |         |   |||||     |         |
          <idle>-0       [001] d.h2. 26650.679279: hrtimer_start: hrtimer=000000003a5aa673 function=tick_sched_timer expires=26651722563925 softexpires=26651722563925 mode=ABS
          <idle>-0       [001] d.h1. 26650.679279: write_msr: 6e0, value 33374f772fbb
          <idle>-0       [001] d.h1. 26650.679279: local_timer_exit: vector=236
          <idle>-0       [001] ..s1. 26650.679279: softirq_entry: vec=7 [action=SCHED]
          <idle>-0       [001] ..s1. 26650.679280: softirq_exit: vec=7 [action=SCHED]
          <idle>-0       [001] ...1. 26650.679416: cpu_idle: state=4294967295 cpu_id=1
          <idle>-0       [001] d..1. 26650.679417: cpu_idle: state=0 cpu_id=1
          <idle>-0       [001] ...1. 26650.679672: cpu_idle: state=4294967295 cpu_id=1

```
