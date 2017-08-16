#!/bin/sh

echo "#include <stdio.h>"
echo "#include <sys/ptrace.h>"
echo
echo "int main()"
echo {
man ptrace | \
    grep -e '^[[:space:]]\+PTRACE_' | \
    tr -d ',.)' | \
    awk '{print $1"\n"$2}' | \
    grep 'PTRACE_' | \
    sort | uniq | \
    grep -v '^PTRACE_EVENT$' | \
    grep -v '^PTRACE_EVENT_STOP$' | \
    grep -v '^PTRACE_SYSEMU$' | \
    grep -v '^PTRACE_SYSEMU_SINGLESTEP$' | \
    awk '{print "    printf(\"" $1 " = %d\\n\"" ", " $1 ");"}'
echo
echo "    return 0;"
echo "}"

