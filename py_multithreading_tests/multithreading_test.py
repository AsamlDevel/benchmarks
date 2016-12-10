#!/usr/bin/python

import sys
import os
import time
import multiprocessing
import thread
import timeit
import skpyext

from time import sleep

usleep = lambda x: time.sleep(x/1000000.0)

NUM_CORES = 4
NUM_TO_INCREMENTS = 100*1000*1000 * NUM_CORES
gcnt = 0

the_lock = thread.allocate_lock()
sem = 0;
def inc_sem():
    global the_lock
    global sem
    the_lock.acquire()
    sem +=1
    the_lock.release()


def incrementor(n,x):

    #print " pythr=%x thr=%x core=%d "%(thread.get_ident(), skpyext.get_cur_thread(), skpyext.cpu_rotate())
    skpyext.stick_thread_to_core(x)

    global gcnt
    i = 0
    while i < NUM_TO_INCREMENTS/NUM_CORES:
        gcnt+=1
        i+=1
    #print "x=%d"%x
    inc_sem()
    pass

def multithreaded_incrementor():
    global gcnt
    gcnt = 0
    for i in xrange(NUM_CORES):
        thread.start_new_thread(incrementor,(i,i))
    ecnt = 0
    while ecnt < NUM_CORES:
        #the_lock.acquire()
        ecnt = sem
        usleep(100)
        
def local_incrementor(n,x):
    #print " pythr=%x thr=%x core=%d "%(thread.get_ident(), skpyext.get_cur_thread(), skpyext.cpu_rotate())
    skpyext.stick_thread_to_core(x)

    lcnt = 0
    i = 0
    while i < NUM_TO_INCREMENTS/NUM_CORES:
        lcnt+=1
        i+=1
    #print "x=%d"%x
    inc_sem()
    pass

def multithreaded_local_incrementor():
    global gcnt
    gcnt = 0
    for i in xrange(NUM_CORES):
        thread.start_new_thread(local_incrementor,(i,i))
    ecnt = 0
    while ecnt < NUM_CORES:
        #the_lock.acquire()
        ecnt = sem
        usleep(100)
        #the_lock.release()
    

def simple_incrementor():
    global gcnt
    gcnt =0
    i = 0
    while i < NUM_TO_INCREMENTS:
        gcnt+=1
        i+=1
    usleep(100)

def main():
    print sys.getcheckinterval()
    #next line is changing python multithreading behavior
    #the argument define the number of instructions before possible next thread switching
    sys.setcheckinterval(1000000)
    print sys.getcheckinterval()
    global gcnt
    global sem
    sem = 0
    print timeit.timeit("multithreaded_incrementor()", setup="from __main__ import multithreaded_incrementor", number=1)/NUM_CORES
    #multithreaded_incrementor()
    print "gcnt1=%d"%gcnt 
    #print "sem=%d"%sem
    print "----------"
    sem = 0
    print timeit.timeit("multithreaded_local_incrementor()", setup="from __main__ import multithreaded_local_incrementor", number=1)/NUM_CORES
    #multithreaded_local_incrementor()
    print "----------" 
    
    print timeit.timeit("simple_incrementor()", setup="from __main__ import simple_incrementor",number=1)/NUM_CORES
    #simple_incrementor()
    print "gcnt2=%d"%gcnt 

    print "the end"
    sys.exit(0)
    pass
    
#-------------------------------------------------
'''Pause before calculate data.'''

wflag = False
rflag = False
x0 = int(0xaaaaaaaaaaaaaaaa)
x1 = x0
x2 = x0

fexit = False

def writer():
    print "CPU #%s" % multiprocessing.current_process().name
    global wflag
    global rflag
    global x0
    global x1
    global x2
    global fexit
    cnt = 0
    x = 0
    while(fexit == False):
        x0^=int(0xffffffffffffffff)
        wflag = True
        cnt = cnt+1 if rflag else cnt
        x1 = x0
        x2 = x0
        #print "%x"%x0
        wflag = False
        x+=1
    
    print "w:%d %d"%(cnt,x)
        
def reader():
    print "CPU #%s" % multiprocessing.current_process().name
    global wflag
    global rflag
    global x0
    global x1
    global x2
    global fexit
    cnt = 0
    nrep = 10*1000*1000
    for i in xrange(nrep):
        if not wflag:
            rflag = True
            cnt = (cnt+1) if x1 != x2 else cnt
            rflag = False    
            
    print "r:%d %d"%(cnt,nrep)
    fexit = True

SLEEP = 1
    
def test2():
    thread.start_new_thread(writer)
    thread.start_new_thread(reader)
    
def getpid():

    '''Checks if there is argument with PID given;
       if is - return PID to other functions.'''

    if len(sys.argv) == 2:
        pid = sys.argv[1]
        return(pid)
    else:
        print('No PID specified. Usage: %s <PID>' % os.path.basename(__file__))
        sys.exit(1)


def proct(pid):

    '''Reads /proc/<pid>/stat file, if extis.
       Get amount of 'utime' (14 item)  and 'stime' (15 item).
       Returns sum of used times by process.'''

    try:
        with open(os.path.join('/proc/', pid, 'stat'), 'r') as pidfile:
            proctimes = pidfile.readline().split(' ')
            utime = proctimes[13]
            stime = proctimes[14]
            return(float(int(utime) + int(stime)))
    except IOError as e:
        print('ERROR: %s' % e)
        sys.exit(2)


def cput():

    '''Reads /proc/stat file, if extis.
       Get amount of:
                   'user'
                   'nice'
                   'system'
                   'idle'
                   'iowait'
                   'irq'
                   'softirq'
                   'steal'
                   'steal'.
        Returns sum of total used times by CPU.'''

    try:
        with open('/proc/stat', 'r') as procfile:
            cputimes = procfile.readline()
            cputotal = 0
            for i in cputimes.split(' ')[2:]:
                i = int(i)
                cputotal = (cputotal + i)
            return(float(cputotal))
    except IOError as e:
        print('ERROR: %s' % e)
        sys.exit(3)


def main2():

    '''First - create start-sum for CPU times and process times.
       pr_proctotal and pr_cputotal - save data from previous iteration.
       While loop - calculates remains between previous and current (proctotal and cputotal) values.
       Rest of times, taken by process, divided to rest of CPU times, to get part of CPU used by process,
       and multiplies to 100, to create %.
       As first loop always return 0 for cputotal - pr_cputotal - it's skipped by `except ZeroDivisionError`.'''
    print multiprocessing.cpu_count()
    print multiprocessing.current_process()

    test2()

    proctotal = proct(getpid())
    cputotal = cput()

    try:
        while True:
            pr_proctotal = proctotal
            pr_cputotal = cputotal

            proctotal = proct(getpid())
            cputotal = cput()

            try:
                res = ((proctotal - pr_proctotal) / (cputotal - pr_cputotal) * 100)
                print('CPU%% %s by PID: %s' % ((round(res, 1)), getpid()))
            except ZeroDivisionError:
                pass

            time.sleep(SLEEP)
    except KeyboardInterrupt:
        print "the end"
        sys.exit(0)
    print "the end xxx"

if __name__ == "__main__":
    main()
