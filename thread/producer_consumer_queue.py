'''
If you want to be able to handle more that one value in the pipeline at a time, you'll need a data structure for the pipeline that allows the number to grow and shrink as data 
backs up from the producer. Python's stardard library has a queue module which, in turn, has a Queue class. Let's change the Pipeline to use a Queue instead of just a variable 
protected by a Lock. You'll also use a different way to stop worker threads by using a different way to stop the worker threads by using different primitive from Python threading, an Event.

Let's start with Event. The threading.Event object allows one thread to signal an event while many other threads can be waiting for that event to happen. The key usage in this code is
that the threads that are waiting for the event do not necessarily need to stop what they are doing, they can just check the status of the Event every once in a while.



'''
import logging
import threading
import concurrent.futures
import time
import random
import queue

class Pipeline(queue.Queue):
    ''' Pipeline is a subclass of queue.Queue. Queue has an optional parameter when initializing to specify a maximum size of the queue. If you give a positive number for maxsize,
        it will limit the queue to that number of elements, causing .put() to block until there are fewer than maxsize elements. If you don't specify maxsize, then the queue will grow
        to the limits of your computer's memory.
        .get_message() and .set_message() got much smaller. They basically wrap .get() and .put() on the Queue. Queue is frequently used in multi-threading environments and incorporated
        all of that locking code inside the Queue itself. Queue is thread-safe.
    '''
    def __init__(self):
        super().__init__(maxsize=10)
    
    def get_message(self, name):
        logging.debug("%s:about to get from queue", name)
        value = self.get()
        logging.debug("%s:got %d from queue", name, value)
        return value

    def set_message(self, value, name):
        logging.debug("%s:about to add %d to queue", name, value)
        self.put(value)
        logging.debug("%s:added %d to queue", name, value)




def producer(pipeline, event): #It will loop until it sees that the event was set on line 3. It also no longer puts the SENTINEL value into the pipeline.
    """ Pretend we're getting a number from the network """
    while not event.is_set():
        message = random.randint(1, 101)
        logging.info("Producer got message: %s", message)
        pipeline.set_message(message, "Producer")
    logging.info("Producer received EXIT event. Exiting.")

def consumer(pipeline, event):
    ''' Pretent we're saving a number in the database'''
    while not event.is_set() or not pipeline.empty():
        message = pipeline.get_message("Consumer")
        logging.info("Consumer storing message: %s  (queue size=%s)", message, pipeline.qsize())
    logging.info("Consumer received EXIT event. Exiting")
''' While you got out the code related to the SENTINEL value, you did have to do a slightly more complicated while condition. Not only does it loop until the event is set,
    but it also needs to keep looping until the pipeline has been emptied.

    If the consumer does exit while the pipeline has message in it, there are two bad things that can happen. The first is that you lose those final messages, but the more serious
    one is that the producer can get cought attempting to add a message to a full queue and never return. This happends if the event gets triggered after the producer has checked the
    .is_set() condition but before it calls pipeline.set_message()
    
    If that happens, it's possible for the producer to wake up and exit with the queue still completely full. The producer will then call .set_message() which will wait until there is
    space on the queue for the new message. The consumer has already exited, so this will not happen and the producer will not exit.
    '''

if __name__ == "__main__": #The triggering of the event can be many things. In this example, the main thread will simply sleep for a while and then .set() it:
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    #logging.getLogger().setLevel(logging.DEBUG)

    pipeline = Pipeline()
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline, event)
        executor.submit(consumer, pipeline, event)

        time.sleep(0.1)
        logging.info("Main: about to set event")
        event.set()
    