import os
import threading
import urllib.request

from time import time, localtime, sleep, strftime
import sched

import winsound

DURATION = 1000 # milliseconds
FREQ = 440 # Hz
FULL_STR_ENCODED = "At this time, all appointments in Massachusetts are booked.".encode()

def check_cvs():
    html = urllib.request.urlopen('https://www.cvs.com/immunizations/covid-19-vaccine').read()

    if FULL_STR_ENCODED not in html:
        for _ in range(50):
            print('APPOINTMENT FOUND!')
            winsound.Beep(FREQ, DURATION)

def daemon(local_handler, t):
    print('Time: {}'.format(strftime('%m/%d/%Y, %H:%M:%S', localtime())))
    check_cvs()
    local_handler.enterabs(t + 10, 1, daemon, (local_handler, t + 10))

def main():
    handler = sched.scheduler(time, sleep)
    t = time()
    handler.enter(0, 1, daemon, (handler, t))
    handler.run()

if __name__ == '__main__':
    main()
