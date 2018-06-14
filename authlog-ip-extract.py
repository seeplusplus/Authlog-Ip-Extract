#!/usr/bin/env python3
import os
import re
import sys

if len(sys.argv) <= 1:
    print("USAGE: authlog-ip-extract /path/to/auth.log")

class LogEntry:
    _regex = "^(\D{3}\s+\d{1,2}\s+.{8}).+(Accepted|Failed) password for (\S+) from (\S+)"
    def BuildEntry(log_text):
        temp = LogEntry()
        re_match = re.match(LogEntry._regex, log_text)
        #if not re_match:
        if not re_match:
            return None
        temp._log_dt = re_match.group(1) 
        temp._log_status = re_match.group(2)
        temp._log_user = re_match.group(3)
        temp._log_ip = re_match.group(4)
        return temp

file = open(sys.argv[1], 'r')

log_entries = [] 
for line in file:
    temp = LogEntry.BuildEntry(line)
    if temp is not None:
        log_entries.append(temp)

for entry in log_entries:
    print(entry)
