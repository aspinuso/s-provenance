import provenance as provenance
import json
import csv
import StringIO
import traceback
import datetime
from prov.model import ProvDocument, Namespace, Literal, PROV, Identifier
from flask import Flask
from flask import request
from flask import Response
from twisted.python import log
app = Flask("s-prov")
global provStore
 

@app.route("/")
def hello():
    return "This is the s-prov service"

@app.route("/activities/<runId>")
def activitiesHandler(runId):
    
    limit = request.args['limit'][0]
    start = request.args['start'][0]
    #if logging == True : log.msg(str(datetime.datetime.now().time())+":GET activities - "+runId);
    response = Response(json.dumps(provStore.getActivities(runId,int(start),int(limit))))
    response.headers['Content-type'] = 'application/json'    
    return response


@app.route("/workflow/summaries")
def summariesHandler():
        
        
        #if logging == True : log.msg(str(datetime.datetime.now().time())+":GET getSummaries - level="+request.args['level'][0]);
        response = Response(json.dumps(provStore.getActivitiesSummaries(**request.args)))
        response.headers['Content-type'] = 'application/json'    
        return response
 
if __name__ == "__main__":
    import sys
    provStore = provenance.ProvenanceStore(sys.argv[1])
    logging=False;
    try:
        if (sys.argv[2]=="True"):
            logging=True
            #print("Logging to webserver.out")
            #log.startLogging(open("webserver.out", 'a'))
        else:
            logging=True
            #print("Logging to stdout")
            #log.startLogging(sys.stdout)
    except:
       logging=False
    
    app.run(debug=True,threaded=True)
    #log.msg("Server running....")
    