import win32service
import win32serviceutil
import os
import sys

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MyNewService"  # Replace with your desired service name
    _svc_display_name_ = "My New Service"  # Replace with a descriptive name

    def __init__(self, *args, **kwargs):
        super(MyService, self).__init__(*args, **kwargs)
        self.script_path = os.path.abspath("test.py")  # Update with your script path

    def start(self):
        # Extract relevant arguments from sys.argv (if needed)
        if len(sys.argv) > 1:
            # Access specific arguments if needed
            argument1 = sys.argv[1]
            # ...

        os.chdir(os.path.dirname(self.script_path))  # Change directory to script location
        os.system(f"python {self.script_path}")  # Execute the script using Python

    def stop(self):
        # Add logic to gracefully stop the script execution,
        # like sending a termination signal or setting a flag.
        pass

if __name__ == "__main__":
    # Manually manage command-line arguments using sys.argv
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "install":
            win32serviceutil.HandleCommandLine(MyService, "install", "--startup=auto")
            print("Service installed successfully.")
        elif command == "start":
            win32serviceutil.StartService(MyService)
            print("Service started successfully.")
        elif command == "stop":
            win32serviceutil.StopService(MyService)
            print("Service stopped successfully.")
        elif command == "uninstall":
            win32serviceutil.uninstall(MyService)
            print("Service uninstalled successfully.")
        else:
            print("Invalid command. Usage: service.py [install|start|stop|uninstall]")
    else:
        print("Usage: service.py [install|start|stop|uninstall]")