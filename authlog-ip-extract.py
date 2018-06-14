#!/usr/bin/env python3
import os
import re
import sys

log_file = ""
if len(sys.argv) <= 1:
    print("USAGE: authlog-ip-extract /path/to/auth.log")
else:
    log_file = sys.argv[1]

class LogEntry:
    _regex = "^(\D{3}\s+\d{1,2}\s+.{8}).+(Accepted|Failed) password for (\S+) from (\S+)"
    def BuildEntry(log_text):
        temp_entry = LogEntry()
        re_match = re.match(LogEntry._regex, log_text)
        #if not re_match:
        if not re_match:
            return None
        temp_entry._log_dt = re_match.group(1) 
        temp_entry._log_status = re_match.group(2)
        temp_entry._log_user = re_match.group(3)
        temp_entry._log_ip = re_match.group(4)
        return temp_entry
    def __str__(self):
        return f"{self._log_dt} {self._log_status} {self._log_user} {self._log_ip}"

def BuildLogFromFile(file_name):
    file = open(file_name, 'r')

    log_entries = [] 

    for line in file:
        temp = LogEntry.BuildEntry(line)
        if temp is not None:
            log_entries.append(temp)
    return log_entries

def PrintReport(log_list):
    report_str = "" 
    for status in {l._log_status for l in log_list}: # for each unique status
        for user in {l._log_user for l in log_list}: # for each unique user
            report_str += f"{status} from {user}\n"
            user_status_ip_sum = {}
            for ip in {l._log_ip for l in log_list}: # for each unique ip
                user_status_ip_sum[ip] = sum(1 for l in log_list if l._log_status == status and l._log_user == user and l._log_ip == ip)
                if user_status_ip_sum[ip]:
                    report_str += f"\t{user_status_ip_sum[ip]} from {ip}\n"
            report_str += f"Total {sum(user_status_ip_sum.values())}\n"
    print(report_str)

log_list = BuildLogFromFile(log_file)
PrintReport(log_list)

