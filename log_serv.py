import tkinter as tk
from tkinter import ttk
import requests
import schedule
import time
from datetime import datetime
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
import tkinter as tk
from tkinter import ttk
import requests
import threading


class App:
    def __init__(self):
        self.corporate_name_entry = None
        self.user_name_entry = None
        self.root = None
        self.error_label = None
        self.token = None

    def get_event_logs(self, server, logtype):
        # Your existing implementation
        hand = win32evtlog.OpenEventLog(server,logtype)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
        DIR = "E:\\systemtrackapp\\log.txt"
        try:
            events=1
            got_login = False
            got_logout = False
            while events:
                events=win32evtlog.ReadEventLog(hand,flags,0)
                for ev_obj in events:
                    if ev_obj.EventID == 4648:
                        the_time = ev_obj.TimeGenerated.Format()
                        # print(ev_obj.StringInserts)
                        # print(ev_obj.TimeGenerated.Format())
                        with open(DIR, "a+") as file:
                            file.write("\n"+ "Entry Date: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
                            file.write("\n" + "token: " + self.token + "\n")
                            file.write("Last login time" + the_time)
                        events=0
                        break
                    # the_time = ev_obj.TimeGenerated.Format() #'12/23/99 15:54:09'
                    # if ev_obj.EventID == 4624 and ev_obj.LogonType==2 and got_login==False:
                    #     with open(DIR, "a+") as file:
                    #         file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
                    #         file.write("Last login time" + the_time)
                    #         got_login = True
                    # elif ev_obj.EventID == 4634 and got_logout == False:
                    #     with open(DIR, "a+") as file:
                    #         file.write("Last logout time" + the_time)
                    #         got_logout = True
                    # if got_login == True and got_logout == True:
                    #     events = 0
        except:
            pass


    def main(self):
        server = "localhost"
        self.get_event_logs(server, "Security")

    def on_submit(self):
        corporate_name = self.corporate_name_entry.get()
        user_name = self.user_name_entry.get()

        # Call your API to get the token (replace with your actual API endpoint)
        api_url = "http://127.0.0.1:8000/create_user_corp_map/"
        payload = {"corporate_name": corporate_name, "user_name": user_name}
        response = requests.post(api_url, data=payload)

        if response.status_code == 201:
            self.token = response.json().get("token")

            # Start the scheduler in a separate thread
            self.scheduler_thread = threading.Thread(target=self.run_scheduler)
            self.scheduler_thread.start()

            # Close the GUI window
            self.root.destroy()
        else:
            # Handle API error
            self.error_label.config(text="Error: Unable to get token")

    def run_scheduler(self):
        while True:
            self.main()  # Run the main function
            time.sleep(5)  # Schedule next run after 5 seconds

    def show_console(self):
        self.root = tk.Tk()
        self.root.title("User Information")

        corporate_name_label = ttk.Label(self.root, text="Corporate Name:")
        self.corporate_name_entry = ttk.Entry(self.root)

        user_name_label = ttk.Label(self.root, text="User Name:")
        self.user_name_entry = ttk.Entry(self.root)

        submit_button = ttk.Button(self.root, text="Submit", command=self.on_submit)

        self.error_label = ttk.Label(self.root, text="", foreground="red")

        corporate_name_label.grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.corporate_name_entry.grid(row=0, column=1, pady=5, padx=5, sticky="w")

        user_name_label.grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.user_name_entry.grid(row=1, column=1, pady=5, padx=5, sticky="w")

        submit_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.error_label.grid(row=3, column=0, columnspan=2)

        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.show_console()