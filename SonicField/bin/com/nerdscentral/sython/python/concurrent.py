import threading
import time
from java.util.concurrent import Executors, TimeUnit
from java.util.concurrent import Callable, Future
from java.lang import System

SF_MAX_CONCURRENT = int(System.getProperty("synthon.threads"))
print "Concurrent Threads: " + SF_MAX_CONCURRENT.__str__()
#SF_POOL = Executors.newFixedThreadPool(SF_MAX_CONCURRENT)
SF_POOL = Executors.newCachedThreadPool()

class sf_callable(Callable):
    def __init__(self,toDo):
        self.toDo=toDo
        
    def call(self):
        return self.toDo()

class sf_getter(Future):
    def __init__(self,toDo):
        self.toDo=toDo

    def get(self):
        return self.toDo()

def sf_do(toDo):
    count=SF_POOL.getActiveCount()
    #print "Thread Count: ",count
    if(count<SF_MAX_CONCURRENT):
        task=sf_callable(toDo)
        return SF_POOL.submit(task)
    else:
        #print "Thread saturation - running inline"
        return sf_getter(toDo)

from java.util.concurrent import TimeUnit

def shutdown_and_await_termination(pool, timeout):
    pool.shutdown()
    try:
        if not pool.awaitTermination(timeout, TimeUnit.SECONDS):
            pool.shutdownNow()
            if (not pool.awaitTermination(timeout, TimeUnit.SECONDS)):
                print >> sys.stderr, "Pool did not terminate"
    except InterruptedException, ex:
        # (Re-)Cancel if current thread also interrupted
        pool.shutdownNow()
        # Preserve interrupt status
        Thread.currentThread().interrupt()
        
def shutdownConcurrnt():
    shutdown_and_await_termination(SF_POOL, 5)