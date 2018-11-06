import datetime
import os

class StopWatch:

    start = None
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.start = datetime.datetime.now()
    
    def read(self, in_seconds=False):
        delta = datetime.datetime.now() - self.start
        if in_seconds:
            return (delta.total_seconds())
        return(delta)