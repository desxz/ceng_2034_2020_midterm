#!/usr/bin/env python
import os
import multiprocessing
import sys
import requests
import threading as Threading
from multiprocessing.dummy import Pool as ThreadPool

urls = ['https://api.github.com/', 'http://bilgisayar.mu.edu.tr/', 'https://www.python.org/',
        'http://akrepnalan.com/ceng2034', 'https://github.com/caesarsalad/wow']

pid = os.getgid()
load1, load5, load15 = os.getloadavg()
nproc = multiprocessing.cpu_count()
osystem = sys.platform

def prtOs():
    print('PID:', pid)
    if osystem == "linux" or osystem == "linux2":                                   #Control the system is linux or not
        print('Load Averages:', os.getloadavg())

    print("Load average over the last 5 minute:", load5)
    print('CPU Core Count:', nproc)
    if nproc - load5 < 1:
        print('Exiting')
        sys.exit()


def statusControl(url):
    r = requests.get(url)
    if r.status_code in range(200, 300):
        print('Status Code:', r.status_code, '|Connection Success|',url)
    elif r.status_code in range(400,600):
        print('Status Code:', r.status_code, '|Connection Failed|',url)


def multiThreadUse():                                                               #Using multithread
    if multiprocessing.cpu_count() > len(urls):                                     #if cpu_count higher then urls count (threads count < 5 ) use threads per every url.
        for i in urls:
            Threading.Thread(target=statusControl, args=(i,)).start()
    else:                                                                           #if cpu_count less then urls count (threads count < 5 ) use all threads in cpu.
        with ThreadPool(multiprocessing.cpu_count()) as p:
            p.map(statusControl, urls)

threads = []

def staticStatusControl():                                                          # To test the time of single thread
    for i in urls:
        r = requests.get(i)
        if r.status_code in [200, 300]:
            print(i, 'Status Code:', r.status_code, '|Connection Successfully|')
        else:
            print(i, 'Status Code:', r.status_code, '|Connection Failed|')


prtOs()
multiThreadUse()