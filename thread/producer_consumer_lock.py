'''
The producer-consumer problem is a standard computer science problem used to look at threading or process synchronization issues. For this example, you are going to imagine a program
that needs to read messages from a network and write them to disk. The program does not request a message when it wants. It must be listening and accept messages as they come in.
The messages will not come in at a regular pace, but will be coming in bursts. This part of the program is called the producer.

On the other side, once you have a message, you need to write it to a database. The database access is slow, but fast enough to keep up to the average pace of the messages. It is not fast
enough to keep up to when a burst of messages comes in. This part is the consumer.

In between the producer and the consumer, you will create a Pipeline that will be the part that changes as you learn about different synchronization objects.

Let's look at a solution using Lock.
'''

#The general desing is that there is a producer thread that reads from the fake network and puts the message into a Pipeline:

import logging
import random
import concurrent.futures
import threading


SENTINEL = object()

class Pipeline:
    '''
    Class to allow a single element pipeline between producer and consumer

    Initializes these three members and then calls .acquire() on the .consumer_lock. This is the state you want to start in. The producer is allowed to add a new message,
    but the consumer needs to wait until a message is present.
    '''
    def __init__(self):
        self.message = 0   #Stores the message to pass
        self.producer_lock = threading.Lock()  #object that restrics access to the message by the producer thread
        self.consumer_lock = threading.Lock()  #object that restrics access to the message by the producer thread
        self.consumer_lock.acquire()
    '''
    .get_message() and .set_message() are nearly opposites. .get_message() calls .acquire() on the consumer_lock. This is the call that will make the consumer wait until a message is ready.
    Once the consumer has acquired the .consumer_lock, it copies out the value in .message and then calls .release() on the .produce_lock. Releasing this lock is what allows the producer
    to insert the next message into the pipeline.

    There is something subtle going on in .get_message(). It might seem tempting to get rid of message and just have the function end with return self.message.
    As soon as consumer calls .producer_lock.release(), it can be swapped out, and the producer can start running. That could happen before .release() returns.
    This means that there is a slight possibility that when the function returns self.message, that could actually be the next message generated, so you would
    lose the first message. This is another example of a race condition. 
    '''
    def get_message(self, name):
        logging.debug("%s: about to acquire getlock", name)
        self.consumer_lock.acquire()
        logging.debug("%s: have getlock", name)
        message = self.message
        logging.debug("%s: about to release setlock", name)
        self.producer_lock.release()
        logging.debug("%s: setlock released", name)
        return message
    '''
    For .set_message(), you can see the opposite side of the transaction. The producer will call this with a message. It will acquire the .producer_lock, set the .message,
    and call.release() on then consumer_lock, which will allow the consumer to read that value.
    '''
    def set_message(self, message, name):
        logging.debug("%s: about to acquire setlock", name)
        self.producer_lock.acquire()
        logging.debug("%s: have setlock", name)
        self.message = message
        logging.debug("%s: about to release getlock", name)
        self.consumer_lock.release()
        logging.debug("%s: getlock released", name)

'''
To generate a fake message, the producer gets a random number between one and one hundred. It calls .set_message() on the pipeline to send it to the consumer.
The producer also uses a SENTINEL value to signal the consumer to stop after it has sent ten values.
'''

def producer(pipeline):
    # Pretened we're getting a message from the network
    for index in range(10):
        message = random.randint(1,101)
        logging.info("Producer got message: %s", message)
        pipeline.set_message(message, "Producer")
    # Send a sentinel message to tell consumer we're done
    pipeline.set_message(SENTINEL, "Producer")


'''
The consumer reads a message from the pipeline and writes is to a fake database, which in this case is just printing it to the display. If it gets the SENTINEL value,
it returns from the function, which will terminate the thread.
'''

def consumer(pipeline):
    ''' Pretend we're saving a number in the database. '''
    message = 0
    while message is not SENTINEL:
        message = pipeline.get_message("Consumer")
        if message is not SENTINEL:
            logging.info("Consumer storing message: %s", message)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    #logging.getLogger().setLevel(logging.DEBUG)
    pipeline = Pipeline()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline)
        executor.submit(consumer, pipeline)