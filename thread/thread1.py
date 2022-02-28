# To start a seperate thread, you create a Thread instance and then tell it to .start()

import logging
# The logging module is intended to be thread-safe without any special work needing to be done by its clients.
# It achieves this though using threading locks.
import threading
import time

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format ="%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S") # Does basic configuration for the logger system by creating a StreamHandler with a default Formatter and adding it to the root logger.
    logging.info("Main    : before creating thread")   # Logs a message with level INFO on this logger. The arguments are interpreted as for debug.
    x = threading.Thread(target=thread_function, args=(1,)) 
    # When you create a thread, you pass it a function and a list containing the arguments to that function. 
    # In this case, you're telling the Thread to run thread_function() and to pass it 1 as an argument.
    logging.info("Main    : before running thread")
    x.start()
    logging.info("Main    : wait for the thread to finish")
    # x.join()
    logging.info("Main    : all done")

