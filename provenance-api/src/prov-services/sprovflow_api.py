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
import logging
import sys
import os
app = Flask(__name__)
app.config['DEBUG'] = True
logging=os.environ['SPROV_LOGGING']

 

def bootstrap_app():
    app.db=provenance.ProvenanceStore(os.environ['SPROV_REPO'])
    return app

@app.route("/")
def hello():
    return "This is the s-prov service"


@app.route("/workflowexecution/<runid>/invocations")
def getInvovocations(runid):
    limit = request.args['limit'] 
    start = request.args['start']
     
    if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET invocations - "+runid+" PID:"+str(os.getpid()));
    response = Response()
    response = Response(json.dumps(app.db.getActivities(runid,int(start),int(limit))))
    response.headers['Content-type'] = 'application/json'    
    return response

@app.route("/workflowexecution/<runid>/invocations/<invocid>")
def getEntitiesByInvocation(runid,invocid):
        limit = int(request.args['limit']) 
        start = int(request.args['start'])
        response = Response()
        response = Response(json.dumps(app.db.getEntitiesGeneratedBy(runid,invocid,start,limit)))
        response.headers['Content-type'] = 'application/json'       
        return response


if __name__ == "__main__":
    import sys
    #app.db = provenance.ProvenanceStore("mongodb://127.0.0.1/verce-prov")
    logging=False;
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(stream_handler)
    app.run()
    # app.logger.info("Server running....")
    