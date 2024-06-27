# Define the source and event IDs
import subprocess
from datetime import datetime, timedelta
import os
import json
import re
import requests
import win32evtlog
import win32evtlogutil
import win32security
from datetime import datetime, timedelta
from copy import deepcopy


source = "Microsoft-Windows-Power-Troubleshooter"
event_ids = [1]

# Get the handle to the event log
hand = win32evtlog.OpenEventLog(None, source)

# Get the time 7 days ago

# Prepare the list to store results
results = []

last_login_time = "2024-06-26T15:00:28"

# Read events from the event log
events = 1
while events:
    events = win32evtlog.ReadEventLog(hand, win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ, 0)
    for event in events:
        if event.SourceName == source and datetime.strptime(event.TimeGenerated.Format(), '%a %b %d %H:%M:%S %Y') > datetime.strptime(last_login_time, '%Y-%m-%dT%H:%M:%S'):
            if event.EventID in event_ids:
                print(event.EventID)
                event_type = "Logon"
                account, _, _ = win32security.LookupAccountSid(None, event.Sid)
                results.append({"Time": datetime.strptime(event.TimeGenerated.Format(), '%a %b %d %H:%M:%S %Y'), "Event": event_type, "User": account})
                print(True)
print("results - ", results)
# Close the event log handle
win32evtlog.CloseEventLog(hand)