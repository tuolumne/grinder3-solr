# The script life cycle
#
# A script that demonstrates how the various parts of a script and
# their effects on worker threads.

# The "top level" of the script is called once for each worker
# process. Perform any one-off initialisation here. For example,
# import all the modules, set up shared data structures, and declare
# all the Test objects you will use.

from net.grinder.script.Grinder import grinder
from net.grinder.plugin.http import HTTPRequest
from net.grinder.script import Test
from java.lang import System
import random



def retrieveWordsFromDictionary():
    words = []
    dictFile = open('words.txt','r');
    for line in dictFile:
        words.append(line)
    return words


def getRandomWordFromDict():
    return  random.choice(words)

words = retrieveWordsFromDictionary()

print "Wordlist count: %s " % len( words)


test1 = Test(1, "Request resource")
request1 = HTTPRequest()
test1.record(request1)


# An instance of the TestRunner class is created for each worker thread.
class TestRunner:

    # The __init__ method is called once for each thread.
    def __init__(self):
        # There's an initialisationTime variable for each worker thread.
        self.initialisationTime = System.currentTimeMillis()
        self.queryTerm = getRandomWordFromDict()
        grinder.logger.info("New thread started at time %s" %
                            self.initialisationTime)

    # The __call__ method is called once for each test run performed by
    # a worker thread.
    def __call__(self):
        # You can also vary behaviour based on thread ID.
        #if grinder.threadNumber % 2 == 0:
        queryTerm = getRandomWordFromDict()
        grinder.logger.info("My request query term is: "+ queryTerm)
        grinder.statistics.delayReports = 1
        #urla = "http://solr3.library.ucsf.edu/solr/ltdl3/select?q=*&wt=json&rows=0&facet=true&facet.mincount=0&facet.pivot=industry,collection_facet&facet.pivot=availability_facet,availabilitystatus_facet&_=1425059929585"
        #urlb = "
        #grinder.logger.info("URL1: %s" %urla)
        #grinder.logger.info("URL2: %s" %urlb)
        
        url = "http://solr3.library.ucsf.edu/solr/ltdl3/select?q=(%s)&wt=json&start=0&rows=50&facet=true&facet.mincount=0&facet.pivot=industry,collection_facet&facet.pivot=availability_facet,availabilitystatus_facet&facet.field=dddate&fq%%3DNOT(pg%%3A1%%20AND%%20(dt%%3A%%22blank%%20document%%22%%20OR%%20dt%%3A%%22blank%%20page%%22%%20OR%%20dt%%3A%%22file%%20folder%%22%%20OR%%20dt%%3A%%22file%%20folder%%20begin%%22%%20OR%%20dt%%3A%%22file%%20folder%%20cover%%22%%20OR%%20dt%%3A%%22file%%20folder%%20end%%22%%20OR%%20dt%%3A%%22file%%20folder%%20label%%22%%20OR%%20dt%%3A%%22file%%20sheet%%22%%20OR%%20dt%%3A%%22file%%20sheet%%20beginning%%22%%20OR%%20dt%%3A%%22tab%%20page%%22%%20OR%%20dt%%3A%%22tab%%20sheet%%22))&facet.field=dt_facet&facet.field=brd_facet&facet.field=dg_facet&hl=true&hl.simple.pre=%%3Ch1%%3E&hl.simple.post=%%3C%%2Fh1%%3E&hl.requireFieldMatch=false&hl.preserveMulti=true&hl.fl=ot,ti&f.ot.hl.fragsize=300&f.ot.hl.alternateField=ot&f.ot.hl.maxAlternateFieldLength=300&f.ti.hl.fragsize=300&f.ti.hl.alternateField=ti&f.ti.hl.maxAlternateFieldLength=300&fq={!collapse%%20field=signature}&expand=true&sort=score+desc,availability_facet+asc&_=1425059929587" %queryTerm.strip()
        

        result = request1.GET(url)

        if ( result.getStatusCode()!=200 ):
            grinder.statistics.forLastTest.setSuccess(0)
        # Sleep for a random amount of time around 1 seconds.
        #grinder.sleep(1000)

    # Scripts can optionally define a __del__ method. The Grinder
    # guarantees this will be called at shutdown once for each thread
    # It is useful for closing resources (e.g. database connections)
    # that were created in __init__.
    def __del__(self):
        grinder.logger.info("Thread shutting down")
