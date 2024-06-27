import os
import sys
import time
from pyuac import main_requires_admin
import schedule
from SMWinservice import SMWinservice
import servicemanager
from datetime import datetime
import requests
import configparser
import win32service
import subprocess
import re


#----------------------------------------------------------------------
#----------------------------------------------------------------------

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
    lst = list(set(lst))
    lst = sorted(lst, reverse=True)
    return lst


def getEventLogs(server, logtype, token):
    """
    Get the event logs from the specified machine according to the
    logtype (Example: Application) and save it to the appropriately
    named log file
    """
    DIR = "E:\\systemtrackapp\\log.txt"
    try:
        file_name = "log_info.txt"
        location = os.path.join(os.path.dirname(sys.executable), file_name)
        if os.path.exists(location):
            with open(location, 'r') as f:
                content = f.read()
            variables = {}
            exec(content, variables)
            last_login_time = variables["last_login_time"]
        else:
            last_login_time = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S")
        
        logoff_command = f'Get-WinEvent -FilterHashtable @{{LogName="Security"; Id=4647; StartTime="{last_login_time}"}}'
        sleep_command = f'Get-WinEvent -FilterHashtable @{{LogName="System"; Id=506; StartTime="{last_login_time}"}}'
        login_command = f'Get-WinEvent -FilterHashtable @{{LogName="Security"; Id=4624; StartTime="{last_login_time}"}} | Where-Object {{ $_.Properties[8].Value -eq 2 }}'
        wake_up_command = f'Get-WinEvent -FilterHashtable @{{LogName="System"; Id=507; StartTime="{last_login_time}"}}'
        login_time_stamps = []
        wake_up_time_stamps = []
        log_off_time_stamps = []
        sleep_time_stamps = []

        try:
            result = subprocess.run(['powershell', '-Command', logoff_command], capture_output=True, text=True, check=True)
            log_off_time_stamps = generate_timestamp_list(result)
        except subprocess.CalledProcessError as e:
            pass

        try:
            result = subprocess.run(['powershell', '-Command', wake_up_command], capture_output=True, text=True, check=True)
            wake_up_time_stamps = generate_timestamp_list(result)
        except subprocess.CalledProcessError as e:
            pass

        try:
            result = subprocess.run(['powershell', '-Command', sleep_command], capture_output=True, text=True, check=True)
            sleep_time_stamps = generate_timestamp_list(result)
        except subprocess.CalledProcessError as e:
            pass

        try:
            result = subprocess.run(['powershell', '-Command', login_command], capture_output=True, text=True, check=True)
            login_time_stamps = generate_timestamp_list(result)
        except subprocess.CalledProcessError as e:
            pass

        new_login_list = wake_up_time_stamps + login_time_stamps
        new_login_list = sorted(new_login_list, reverse=True)
        new_logout_list = sleep_time_stamps + log_off_time_stamps
        new_logout_list = sorted(new_logout_list, reverse=True)
        for x in new_login_list:
            if x in new_logout_list:
                new_logout_list = [i for i in new_logout_list if i!=x]
        new_login_list = [datetime.strptime(timestamp, '%d-%m-%Y %H:%M:%S') for timestamp in new_login_list]
        new_logout_list = [datetime.strptime(timestamp, '%d-%m-%Y %H:%M:%S') for timestamp in new_logout_list]
        last_login_time = new_login_list[0] if new_login_list else last_login_time
        login_logout_list = []
        j=0
        length_of_logout_list = len(new_logout_list)
        if new_login_list and new_logout_list:
            for x in new_login_list:
                if x > new_logout_list[j]:
                    login_logout_list.append([x, new_logout_list[j]])
                elif abs((x - new_logout_list[j]).total_seconds()) <= 2:
                    continue
                else:
                    if j+1 == length_of_logout_list:
                        break
                    j+=1
                    login_logout_list.append([x, new_logout_list[j]])
        
        if login_logout_list:
            formatted_login_logout_list = [
                [dt.strftime("%Y-%m-%dT%H:%M:%S") for dt in pair]
                for pair in login_logout_list
            ]
            data = {
                "token": token,
                "timestamps_list": formatted_login_logout_list
            }
            try:
                requests.post(url="http://127.0.0.1:8000/create_user_time_stamps/", json=data)
                with open(location, 'w') as f:
                    f.write(f'last_login_time = "{last_login_time}"\n')
            except Exception:
                pass


        with open(DIR, 'a+') as f:
            for x in login_logout_list:
                f.write(str(x) + "\n")
            f.write("\n")
            f.write("-----------------")
            f.write("\n")

    except Exception as e:
        pass


@main_requires_admin
def main(token):
    server = "localhost"
    getEventLogs(server, "Security", token)


# run_scheduler()


class PythonCornerExample(SMWinservice):
    _svc_name_ = "Background Login Log Service"
    _svc_display_name_ = "Log Login Time"
    _svc_description_ = "That's a great winservice! :)"
    _svc_start_type_ = win32service.SERVICE_AUTO_START

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        exe_dir = os.path.dirname(sys.executable)
        config_path = os.path.join(exe_dir, "service_config.ini")
        config = configparser.ConfigParser()
        config.read(config_path)
        token = config.get("DEFAULT", "token", fallback=None)
        schedule.every(15).seconds.do(lambda: main(token))

        while self.isrunning:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                pass


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(PythonCornerExample)
        servicemanager.StartServiceCtrlDispatcher()
        x=input()
    else:
        PythonCornerExample.parse_command_line()