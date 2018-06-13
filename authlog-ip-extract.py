#!/usr/bin/env python3
import os
import re
import pandas as pd
import numpy as np
import sys
regex = '^(\D{3}\s+\d{1,2}\s+.{8}).+(Accepted|Failed) password for (\S+) from (\S+)'

if len(sys.argv) <= 1:
    print("USAGE: authlog-ip-extract /path/to/auth.log")

print(sys.argv[1])
file = open(sys.argv[1], 'r')
login_df = pd.DataFrame()

for line in file:
    lm = re.match(regex, line)
    if not lm:
        continue
    login_df = login_df.append({'Date':lm.group(1), 'Status':lm.group(2), 
                     'Username':lm.group(3), 'IP Address':lm.group(4)}, ignore_index = True)


login_df['Date'] = pd.to_datetime(str(pd.Timestamp.today().year) + login_df['Date'],
                                   format='%Y%b %d %H:%M:%S', errors='ignore')

GB = login_df.groupby(['Username', 'IP Address', 'Status'])
m = pd.DataFrame(GB.agg({'Date': np.max,
        'Status': 'count'}))

print(m)
