from datetime import datetime

class CountsPerSec:
    '''
    Class that tracks the number of occurences ("counts") of an arbitrary event and returns the frequency in occurrences (counts) per second.
    The caller must increment the count.
    '''
    def __init__(self):
        self._start_time = None
        self._num_occurences = 0

    def start(self):
        self._start_time = datetime.now()
        return self
    def increment(self):
        self._num_occurences += 1
    def countsPerSec(self):
        elapsed_time = (datetime.now() - self._start_time).total_seconds()
        if elapsed_time > 0:
            return self._num_occurences / elapsed_time
        else:
            return 1
