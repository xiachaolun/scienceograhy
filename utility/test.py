import psutil

PROCNAME = "python.exe"

for proc in psutil.process_iter():
    print proc.name()
    # if proc.name() == PROCNAME:
    #     proc.kill()