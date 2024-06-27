import win32evtlog
import win32evtlogutil
import win32security
from datetime import datetime, timedelta

# Define the source and event IDs
source = "Microsoft-Windows-Winlogon"
event_ids = [7001, 7002]

# Get the handle to the event log
hand = win32evtlog.OpenEventLog(None, source)

# Get the time 7 days ago
delta = timedelta(days=7)
start_time = datetime.now() - delta

# Prepare the list to store results
results = []

# Read events from the event log
events = 1
while events:
    events = win32evtlog.ReadEventLog(hand, win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ, 0)
    for event in events:
        if event.SourceName == source and event.TimeGenerated >= start_time:
            if event.EventID in event_ids:
                event_type = "Logon" if event.EventID == 7001 else "Logoff"
                account, _, _ = win32security.LookupAccountSid(None, event.Sid)
                results.append({"Time": datetime.strptime(event.TimeGenerated.Format(), '%a %b %d %H:%M:%S %Y'), "Event": event_type, "User": account})

# Close the event log handle
win32evtlog.CloseEventLog(hand)

# Print results
for result in results:
    print(result)