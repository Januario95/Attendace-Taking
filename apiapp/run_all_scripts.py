import os
import threading

X = lambda s: os.system(s)


def Run_ManagePY_Server():
    X('python ../manage.py runserver')

def Main_Program_Script():
    X('python Main_Program.py')

def Presence_Monitoring_Script():
    X('python Main_Program_Attendance.py')

def Check_Out_Script():
    X('python check_out.py')

thread1 = threading.Thread(target=Run_ManagePY_Server)
thread1.start()

thread2 = threading.Thread(target=Main_Program_Script)
thread2.start()

thread3 = threading.Thread(target=Presence_Monitoring_Script)
thread3.start()

thread4 = threading.Thread(target=Check_Out_Script)
thread4.start()


