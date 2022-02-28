'''
Race conditions can occur when two or more threads access a shared piece of data or resource. In this example, you're going to create a large race condition
that happens every time, but be aware that most race conditions are not this obvious. Frequently, they only occur rarely, and they can produce confusing results.
For this example, you're going to write a class that updates a database.
'''

import logging
import time
import concurrent.futures
import threading

class FakeDatabase:
    '''
    It is keeping track of a single number: value. This is going to be the shared data on which you'll see the race condition.
    .update() is simulating reading a value from a database, doing some computations on it, and then writing a new value back to the database.
    
    The program creates a ThreadPoolExecutor with two threads and then calls .submit() on each of them, telling them to run database.update()
    .submit() has a signature that allows both positional and named arguments to be passed to the function running in the thread like .submit(function, *args, **kwargs)
    Since each thread runs .update(), and .update() adds one to .value, you might expect database.value to be 2 when it's printed out at the end. But it is not the case.
    
    When you tell your ThreadPoolExecutor to run each thread, you tell it which function to run and what parameters to pass to it: executor.submit(database.update, index)
    The result of this is that each of the threads in the pool will call database.update(index). Calling .update() on that object calls an instance method on that object.
    Each thread is going to have a reference to the same FakeDatabase object, database. Each thread will also have a unique value, index, to make the logging statements 
    a bit easier to read.

    When the thread starts running .update(), it has its own version of all of the data local to the function. In the case .update(), this is local_copy. This is a good thing.
    Otherwise, two threads running the same function would always confuse each other. It means that all variables that are scoped (or local) to a function are thread-safe.

    The two threads have interleaving access to a single shared object, overwriting eachothers results. Similar race conditions can arise when one thread frees memory or closes
    a file handle before the other thread is finishing accessing it.
    '''
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()
    def update(self, name):
        logging.info("Thread %s: starting update", name)
        local_copy = self.value
        local_copy += 1
        time.sleep(0.1)
        self.value = local_copy
        logging.info("Thread %s: finishing update", name)

    '''
    There are number of ways to avoid or solve race conditions. Let's start with lock. To solve the race condition here, you need to find a way to allow only one thread at a time
    into the read-modifiy-write section of your code. The most common way to do this is called Lock in python. A Lock is an object that acts like a hall pass. Only one thread at a time
    can have Lock. Any other thread that wants the Lock must wait until the owner of the Lock gives it up. 
    The basic functions to do this are .acquire() and .release(). A thread will call my_lock.acquire() to get the lock. If the lock is already held, the calling thread will wait until 
    it is released. There is an important point here. If one thread gets the lock but never gives it back, your program will be stuck.

    Fortunately, Python's Lock will also operate as a context manager, so you can use it in a with statement, and it gets released automatically when the with block exits for any reason.
    
    '''
    # Let's add Lock to the class
    def locked_update(self, name):
        logging.info("Thread %s: starting update", name)
        logging.debug("Thread %s about to lock", name) # Logs a message with level DEBUG on the root logger. The message format is string, and the args are the arguments which are merged
        # into message using the string formatting operator.
        with self._lock:
            logging.debug("Thread %s has lock", name)
            local_copy = self.value
            local_copy += 1
            time.sleep(0.1)
            self.value = local_copy
            logging.debug("Thread %s about to release lock", name)
        logging.debug("Thread %s after release", name)
        logging.info("Thread %s: finishing update", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    database = FakeDatabase()

    logging.info("Testing update with normal update. Starting value is %d", database.value)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for index in range(2):
            executor.submit(database.update, index)
    logging.info("Testing update with normal update. Ending value is %d", database.value)

    logging.info("Testing update with locked update. Starting value is %d", database.value)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for index in range(2):
            executor.submit(database.locked_update, index)
    logging.info("Testing update with locked update. Ending value is %d", database.value)
