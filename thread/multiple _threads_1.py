import logging
import threading
import time
# The harder way of starting multiple threads
# In this way, the order in which threads are run is determined by the operating system and can be quite hard to predict.






def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    threads = list()
    for index in range(3):
        logging.info("Main    : create and start thread %d.", index)
        x = threading.Thread(target=thread_function, args=(index,))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)

print("------------------------------------------")
# There is an easier wat to start up a group of threads. Its called a ThreadPoolExecutor, and its part of the standard library in concurrent.futures
import concurrent.futures

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    executor.map(thread_function, range(3))
# The code creates a ThreadPoolExecutor as a context manager, telling it how many worker threads it wants in the pool. It then uses .map() to step through an iterable of things.
# The end of the with block causes the ThreadPoolExecutor to do a .join() on each of the threads in the pool. It is strongly recommanded that to use it as a context manager
# when you can so that you never forget to .join() the threads.