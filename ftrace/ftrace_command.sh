#!/bin/sh

# nop: 기본 트레이서로, ftrace 이벤트만 출력 
# function: 함수 트레이서로, set_ftrace_filter로 지정한 함수를 누가 호출하는지 출력한다.
# graph_function: 함수 실행 시간과 세부 호출 정보를 그래프 포맷으로 출력
echo function > /sys/kernel/debug/tracing/current_tracer
sleep 1

echo $$ > /sys/kernel/debug/tracing/set_ftrace_pid
sleep 1

# 파일에 트레이싱하고 싶은 함수를 지정: 현재 트레이서를 function_graph과 function로 설정할 경우 작동하는 파일
# 주의!!!) 리눅스 커널에 존재하는 모든 함수를 필터로 지정할 수는 없고 available_filter_functions 파일에 포함된 함수만 지정할 수 있다
# set_ftrace_filter 파일에 필터로 함수를 지정하지 않으면 모든 커널 함수를 트레이싱하여 락업 상태에 빠질 수 있다
# echo  schedule ttwu_do_wakeup > /sys/kernel/debug/tracing/set_ftrace_filter

# ftrace에서 콜스택을 출력할 때 포맷을 지정: 함수를 호출할 때 주소 오프셋을 출력
# echo 1 > /sys/kernel/debug/tracing/options/func_stack_trace
# echo 1 > /sys/kernel/debug/tracing/options/sym-offset

echo 1 > /sys/kernel/debug/tracing/tracing_on
sleep 1

exec $*
echo 0 > /sys/kernel/debug/tracing/tracing_on
