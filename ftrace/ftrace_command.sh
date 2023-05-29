#!/bin/sh

echo function > /sys/kernel/debug/tracing/current_tracer
sleep 1
echo $$ > /sys/kernel/debug/tracing/set_ftrace_pid
sleep 1
echo 1 > /sys/kernel/debug/tracing/tracing_on
sleep 1
exec $*
echo 0 > /sys/kernel/debug/tracing/tracing_on
