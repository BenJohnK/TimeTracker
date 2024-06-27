import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    print("hello")
    x=input()
    with open("sample.txt", "w") as f:
        f.write("simple")

if is_admin():
    main()
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1, nshow=5)
