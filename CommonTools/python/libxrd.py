#!/usr/bin/env python

# Functions to list up catTuple
import sys

## Check xrd command
import subprocess
if subprocess.call("type xrd", shell=True, 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE) != 0:
    print "Error: Need xrd command"
    sys.exit()

def guessxrd():
    import os
    hostname = os.environ["HOSTNAME"]
    cmd = ""
    xrdbase = ''
    xrdhost = ''
    if "sdfarm" in hostname:
        xrdhost = 'cms-xrdr.sdfarm.kr'
        xrdbase = '/xrd'
    elif "uos" in hostname:
        xrdhost = 'uosaf0007.sscc.uos.ac.kr'
        xrdbase = '/cms'
    elif "lxplus" in hostname:
        xrdhost = 'cms-xrd-global.cern.ch'
        xrdbase = ''
    elif "knu" in hostname:
        xrdhost = 'cluster142.knu.ac.kr'
        xrdbase = ''
    else:
        print "Hostname", hostname, "not supported"
        sys.exit()
    if "knu" in hostname: cmd = "xrdfs %s ls " % (xrdhost)
    else: cmd = "xrd %s ls " % (xrdhost)
    return cmd, xrdbase

def listxrd(path):
    import os
    hostname = os.environ["HOSTNAME"]
    knu = False
    if "knu" in hostname: knu = True

    cmd, xrdbase = guessxrd()
    size = 0
    l = set()
    for x in subprocess.check_output(cmd + xrdbase + path, shell=True).strip().split('\n'):
        xx = x.split()
        if len(xx) == 0: continue
        if not knu:
          if xx[0][0] not in ('d', '-'): continue
        xpath = xx[-1]
        if len(xpath) == 0: continue
        if not knu:
          xsize = int(xx[1])
        if xpath.startswith(xrdbase): xpath = xpath[len(xrdbase):]
        if xpath in l: continue
        l.add(xpath)
        if not knu:
          size += xsize
    return l, size


