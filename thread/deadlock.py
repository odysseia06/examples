import threading 

l = threading.Lock()
print("before first acquire")
l.acquire()
print("before second acquire")
l.acquire()
print("acquired lock twice")

'''
If the Lock has already been acquired, a second call to .acquire() will wait until the thread that is holding the Lock calls .release().
When the program calls l.acquire() the second time, it hangs waiting for the Lock to be released. In this example, you can fix the deadlock by removing the second call,
but deadlocks usually happen from one of two subtle things:
1. An implementation bug where a Lock is not released properly
2. A design issue where a utility function needs to be called by functions that might or might not already have the Lock

The first situation happens sometimes, but using Lock as a context manager greatly reduces how often. It is recommended to write code whenever possible to make use of context managers,
as they help to avoid situations where an exception skips you over the .release() call.

Python threading has a second object, called RLock, designed for this situations. It allows a thread to .acquire() an RLock multiple times before it calls .release(). That thread is
still required to call .release() the same number of times it called .acquire(), but it should be doing that anyway.

Lock and RLock are two of the basic tools used in threaded programming to prevent race conditions. There are a few other that work in different ways.
'''

