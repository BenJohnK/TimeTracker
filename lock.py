from collections import defaultdict
from enum import Enum
import win32api
import win32con
import win32gui
import win32ts
from datetime import datetime


class SessionEvent(Enum):
    SESSION_LOCK = 0x7
    SESSION_UNLOCK = 0x8

class WorkstationMonitor:
    CLASS_NAME = "WorkstationMonitor"
    WINDOW_TITLE = "Workstation Event Monitor"

    def __init__(self):
        self.window_handle = None
        self.event_handlers = defaultdict(list)
        self.log_file = "lock_logs.log"
        self._register_listener()


    def _register_listener(self):
        wc = win32gui.WNDCLASS()
        wc.hInstance = handle_instance = win32api.GetModuleHandle(None)
        wc.lpszClassName = self.CLASS_NAME
        wc.lpfnWndProc = self._window_procedure
        window_class = win32gui.RegisterClass(wc)

        style = 0
        self.window_handle = win32gui.CreateWindow(window_class,
                                                   self.WINDOW_TITLE,
                                                   style,
                                                   0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                                   0, 0, handle_instance, None)
        win32gui.UpdateWindow(self.window_handle)

        scope = win32ts.NOTIFY_FOR_ALL_SESSIONS
        win32ts.WTSRegisterSessionNotification(self.window_handle, scope)

    def listen(self):
        win32gui.PumpMessages()

    def stop(self):
        exit_code = 0
        win32gui.PostQuitMessage(exit_code)

    def _window_procedure(self, window_handle: int, message: int, event_id, session_id):
        if message == 0x2B1:  # WM_WTSSESSION_CHANGE
            if event_id == 7:
                self._handle_session_change(SessionEvent(event_id), session_id)
            elif event_id == 8:
                self._handle_session_change(SessionEvent(event_id), session_id)
        elif message == win32con.WM_CLOSE:
            win32gui.DestroyWindow(window_handle)
            return 0  # Return an integer value
        elif message == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0  # Return an integer value
        elif message == win32con.WM_QUERYENDSESSION:
            return 1  # Indicate whether the application can end the session
        return win32gui.DefWindowProc(window_handle, message, event_id, session_id)

    def _handle_session_change(self, event: SessionEvent, session_id: int):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f:
            if event == SessionEvent.SESSION_LOCK:
                f.write(f"Session locked at {current_time}\n")
            elif event == SessionEvent.SESSION_UNLOCK:
                f.write(f"Session unlocked at {current_time}\n")
        for handler in self.event_handlers[event]:
            handler(event)

    def register_handler(self, event: SessionEvent, handler: callable):
        self.event_handlers[event].append(handler)

if __name__ == '__main__':
    m = WorkstationMonitor()
    m.register_handler(SessionEvent.SESSION_LOCK, handler=print)
    m.register_handler(SessionEvent.SESSION_UNLOCK, handler=print)
    m.listen()