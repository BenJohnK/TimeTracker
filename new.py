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

def generate_timestamp_list(result):
    lst = []
    output = result.stdout.splitlines()
    for line in output:
        columns = line.split()
        if len(columns) >= 2:
            time_created = columns[0] + ' ' + columns[1]
            lst.append(time_created)

    timestamp_pattern = r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}'

# Filter the lines containing timestamp strings using the regular expression
    lst = [line.strip() for line in lst if re.match(timestamp_pattern, line)]
    # lst = list(set(lst))
    # lst = sorted(lst, reverse=True)
    lst = [datetime.strptime(timestamp, '%d-%m-%Y %H:%M:%S') for timestamp in lst]
    return lst

def get_win_event(log_name, event_id, start_date_time):
    file_name = "log_info.txt"
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            content = f.read()
        variables = {}
        exec(content, variables)
        last_login_time = variables["last_login_time"]
        print(last_login_time)

    else:
        last_login_time = datetime.today.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S")
        pass

    with open(file_name, 'w') as f:
        f.write(f'last_login_time = "{last_login_time}"\n')


    logoff_command = f'Get-WinEvent -FilterHashtable @{{LogName="Security"; Id=4647; StartTime="{last_login_time}"}}'
    sleep_command = f'Get-WinEvent -FilterHashtable @{{LogName="System"; Id=566; StartTime="{last_login_time}"}}'
    login_command = f'Get-WinEvent -FilterHashtable @{{LogName="Security"; Id=4624; StartTime="{last_login_time}"}} | Where-Object {{ $_.Properties[8].Value -eq 2 }}'
    wake_up_command = f'Get-WinEvent -FilterHashtable @{{LogName="System"; Id=566; StartTime="{last_login_time}"}}'
    login_time_stamps = []
    wake_up_time_stamps = []
    log_off_time_stamps = []
    sleep_time_stamps = []

    try:
        result = subprocess.run(['powershell', '-Command', wake_up_command], capture_output=True, text=True, check=True)
        wake_up_time_stamps = generate_timestamp_list(result)
        output = result.stdout
        with open('wakep.txt', 'w') as f:
            f.write(output)
        print(wake_up_time_stamps)
    except subprocess.CalledProcessError as e:
        print(f'Error: {e}')

    try:
        result = subprocess.run(['powershell', '-Command', sleep_command], capture_output=True, text=True, check=True)
        output = result.stdout
        sleep_time_stamps = generate_timestamp_list(result)
        sleep_time_stamps = [x for x in sleep_time_stamps if x > datetime.strptime(last_login_time, '%Y-%m-%dT%H:%M:%S')]
        with open('sleep.txt', 'w') as f:
            f.write(output)
        print(sleep_time_stamps)
    except subprocess.CalledProcessError as e:
        print(f'Error: {e}')

    # Define the source and event IDs
    source = "Microsoft-Windows-Winlogon"
    event_ids = [7001, 7002]

    # Get the handle to the event log
    hand = win32evtlog.OpenEventLog(None, source)

    # Get the time 7 days ago

    # Prepare the list to store results
    results = []

    # Read events from the event log
    events = 1
    while events:
        events = win32evtlog.ReadEventLog(hand, win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ, 0)
        for event in events:
            if event.SourceName == source and datetime.strptime(event.TimeGenerated.Format(), '%a %b %d %H:%M:%S %Y') > datetime.strptime(last_login_time, '%Y-%m-%dT%H:%M:%S'):
                if event.EventID in event_ids:
                    event_type = "Logon" if event.EventID == 7001 else "Logoff"
                    account, _, _ = win32security.LookupAccountSid(None, event.Sid)
                    results.append({"Time": datetime.strptime(event.TimeGenerated.Format(), '%a %b %d %H:%M:%S %Y'), "Event": event_type, "User": account})
    print("results - ", results)
    # Close the event log handle
    win32evtlog.CloseEventLog(hand)

    for result in results:
        if result['Event'] == "Logon":
            login_time_stamps.append(result['Time'])
        elif result['Event'] == "Logoff":
            log_off_time_stamps.append(result['Time'])


    new_login_list = wake_up_time_stamps + login_time_stamps
    new_login_list = sorted(new_login_list)
    with open('login_file.txt', 'w') as f:
        for x in new_login_list:
            f.write(str(x) + "\n")
    new_logout_list = sleep_time_stamps + log_off_time_stamps
    new_logout_list = sorted(new_logout_list)
    print("here")
    print(new_logout_list)
    temp_logout_list = deepcopy(new_logout_list)
    for x in new_login_list:
        if x in new_logout_list:
            index = new_logout_list.index(x)
            print("index", index)
            new_logout_list.pop(index)
    #     if x-timedelta(seconds=1) in new_logout_list:
    #         index = new_logout_list.index(x-timedelta(seconds=1))
    #         print("index", index)
    #         new_logout_list.pop(index)
    print("cutted lo")
    with open('logout_file.txt', 'w') as f:
        for x in new_logout_list:
            f.write(str(x) + "\n")

    login_logout_list = []
    j=0
    if new_login_list and new_logout_list:
        for i in range(len(new_login_list)):
            for j in range(len(new_logout_list)):
                if new_login_list[i] < new_logout_list[j]:
                    login_logout_list.append([new_login_list[i], new_logout_list[j]])
                    break
    
    
    
    if login_logout_list:
    #     for i in range(len(login_logout_list)):
    #         if login_logout_list[i][0] < login_logout_list[i][1]:
    #             try:
    #                 temp1 = [login_logout_list[i-1][0], login_logout_list[i][1]]
    #                 temp2 = [login_logout_list[i][0], login_logout_list[i+1][1]]
    #                 temporary_list.append(temp1)
    #                 temporary_list.append(temp2)
    #             except Exception:
    #                 continue
    #     login_logout_list.extend(temporary_list)
    #     login_logout_list = sorted(login_logout_list, key=lambda x: x[0], reverse=True)
    #     for x in login_logout_list:
    #         if x[0] < x[1]:
    #             login_logout_list.remove(x)
    
        deduped_data = {}
        for sublist in login_logout_list:
            deduped_data[sublist[1]] = sublist

        login_logout_list = list(deduped_data.values())
        formatted_login_logout_list = [
            [dt.strftime("%Y-%m-%dT%H:%M:%S") for dt in pair]
            for pair in login_logout_list
        ]
        print(len(formatted_login_logout_list))
        print(formatted_login_logout_list)
    #     deduped_data = {}
    #     for x in login_logout_list:
    #         deduped_data[x[0]] = x[1]
    #     print(deduped_data)
    #     for k in deduped_data:
    #         deduped_login_logout_list.append([k, deduped_data[k]])
        # for x in login_logout_list:
        #     if x[1] + timedelta(seconds=1) in wake_up_time_stamps:
        #         print("item", x)
        #         if x[1] + timedelta(seconds=1) not in temp_logout_list:
        #             login_logout_list.remove(x)
    
            

    formatted_login_logout_list = [
        [dt.strftime("%Y-%m-%dT%H:%M:%S") for dt in pair]
        for pair in login_logout_list
    ]
    data = {
        "token": "123",
        "timestamps_list": formatted_login_logout_list
    }
    with open('final_output.txt', 'w') as f:
        for x in formatted_login_logout_list:
            print(x)
        
    # requests.post(url="http://127.0.0.1:8000/create_user_time_stamps/", json=data)
    with open('final_output.txt', 'w') as f:
        json.dump(data, f)


# Example usage:
log_name = "Security"
event_id = 4624
start_date_time = "2024-03-17T00:00:25"
end_date_time = datetime.now()
events = get_win_event(log_name, event_id, start_date_time)
# if events:
#     print(events)
# else:
#     print("No events found.")