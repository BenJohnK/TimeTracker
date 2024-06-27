import codecs
from contextlib import redirect_stderr
import os
import sys
import time
import traceback
import win32con
import win32evtlog
import win32evtlogutil
import winerror
from pyuac import main_requires_admin
import schedule
from pathlib import Path
from SMWinservice import SMWinservice
import servicemanager
import win32serviceutil
from datetime import datetime

#----------------------------------------------------------------------
#----------------------------------------------------------------------

def main():
    DIR = "E:\\systemtrackapp\\log.txt"
    with open(DIR, "a+") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")


def run_scheduler():
    schedule.every(5).seconds.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)

# run_scheduler()

class PythonCornerExample(SMWinservice):
    _svc_name_ = "Background Login Log Service"
    _svc_display_name_ = "Log Login Time"
    _svc_description_ = "That's a great winservice! :)"

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        run_scheduler()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(PythonCornerExample)
        servicemanager.StartServiceCtrlDispatcher()
        x=input()
    else:
        PythonCornerExample.parse_command_line()