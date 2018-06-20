#!/usr/bin/env python3
import re
from os.path import isfile
import sys
from datetime import datetime as dt


class LogEntry:
    _regex = "^(\D{3}\s+\d{1,2}\s+.{8}).+(Accepted|Failed) password for (\S+) from (\S+)"
    _dt_str_format = "%b %d %H:%M:%S"

    def build_entry(log_text):
        temp_entry = LogEntry()
        re_match = re.match(LogEntry._regex, log_text)
        if not re_match:
            return None
        temp_dt_str = re_match.group(1)
        try:
            temp_entry.log_dt = dt.strptime(temp_dt_str, LogEntry._dt_str_format)
        except ValueError:
            temp_entry.log_dt = temp_dt_str
        temp_entry.log_status = re_match.group(2)
        temp_entry.log_user = re_match.group(3)
        temp_entry.log_ip = re_match.group(4)
        return temp_entry

    def __str__(self):
        return f"{self.log_dt} {self.log_status} {self.log_user} {self.log_ip}"


def build_log_from_file(file_name):
    log_entries = []
    with open(file_name, 'r') as file:
        for line in file:
            temp = LogEntry.build_entry(line)
            if temp is not None:
                log_entries.append(temp)
    return log_entries


def print_report(log_list):
    report_str = ""
    for status in sorted({l.log_status for l in log_list}): # for each unique status
        for user in sorted({l.log_user for l in log_list}): # for each unique user
            report_str += f"{status} from {user}\n"
            user_status_ip_sum = {}
            for ip in sorted({l.log_ip for l in log_list}): # for each unique ip
                user_status_ip_sum[ip] = sum(1 for l in log_list if l.log_status == status and l.log_user == user and
                                             l.log_ip == ip)
                if user_status_ip_sum[ip]:
                    dt_str = ""
                    try:
                        last_login_dt = max(l.log_dt for l in log_list if l.log_user == user
                                            and l.log_status == status and l.log_ip == ip)
                        dt_str = f"({last_login_dt.strftime(LogEntry._dt_str_format)})"
                    finally:
                        report_str += f"\t{user_status_ip_sum[ip]} from {ip} {dt_str}\n"

            report_str += f"Total {sum(user_status_ip_sum.values())}\n"
    print(report_str)


log_file = ""
if len(sys.argv) <= 1 or not (isfile(sys.argv[1])):
    print("USAGE: authlog-ip-extract /path/to/auth.log")
    sys.exit(-1)
else:
    log_file = sys.argv[1]

log_list = build_log_from_file(log_file)
print_report(log_list)

