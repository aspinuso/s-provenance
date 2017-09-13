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
logging=os.environ['RAAS_LOGGING']

 

def bootstrap_app():
    app.db=provenance.ProvenanceStore(os.environ['RAAS_REPO'])
    return app

@app.route("/")
def hello():
    return "This is the s-prov service"

@app.route("/activities/<runId>")
def activitiesHandler(runId):
    limit = request.args['limit'] 
    start = request.args['start']
     
    if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET activities - "+runId+" PID:"+str(os.getpid()));
    response = Response()
    response = Response(json.dumps(app.db.getActivities(runId,int(start),int(limit))))
    response.headers['Content-type'] = 'application/json'    
    return response


@app.route("/workflow/")
def workflowsHandler():
        print "ADA"
        response = Response(json.dumps(app.db.getWorkflows(**request.args)))
        response.headers['Content-type'] = 'application/json'
        return response
    
@app.route("/workflow/user/<user>")  
def getUserRuns(user):
        
        keylist = None
        vluelist= None
        mxvaluelist= None
        mnvaluelist= None
       
        limit = request.args['limit']
        start = request.args['start']
         
         
        try:
            memory_file = StringIO.StringIO(request.args['keys']);
            keylist = csv.reader(memory_file).next()
            
            memory_file = StringIO.StringIO(request.args['maxvalues']);
            mxvaluelist = csv.reader(memory_file).next()
            memory_file = StringIO.StringIO(request.args['minvalues']);
            mnvaluelist = csv.reader(memory_file).next()
            
        except Exception, err:
            None
            
         
        if (keylist==None and 'activities' not in request.args):
            
            if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET getUserRuns - "+user+" PID:"+str(os.getpid()));
            response = Response(json.dumps(app.db.getUserRuns(user,**request.args)))
            response.headers['Content-type'] = 'application/json'
            return response
        else:
             
            if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":GET getUserRunsValuesRange - "+user+" PID:"+str(os.getpid()));
            response = Response(json.dumps(app.db.getUserRunsValuesRange(user,keylist,mxvaluelist,mnvaluelist,**request.args)))
            response.headers['Content-type'] = 'application/json'
            return response
        

@app.route("/workflow/edit/<runid>", methods=['POST'])
def workflowInfoHandlerEdit(runid):
        
        #if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":POST WorkflowRunInfo - "+runid);
        print(request.form)
        response = Response(json.dumps(app.db.editRun(runid,json.loads(str(request.form["doc"])))))
        response.headers['Content-type'] = 'application/json'
        return response
    

@app.route("/workflow/delete/<runid>", methods=['POST'])
def workflowInfoHandlerDelete(runid):
         
        if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":POST WorkflowRunInfo - "+runid+" PID:"+str(os.getpid()));
        print(request.form)
        response = Response(json.dumps(app.db.deleteRun(runid)))
        response.headers['Content-type'] = 'application/json'
        return response

@app.route("/workflow/insert", methods=['POST'])
def insertData():
        payload = request.form["prov"] if "prov" in request.form else request.content.read()
        payload = json.loads(str(payload))
        response = Response(json.dumps(app.db.insertData(payload)))
        response.headers['Content-type'] = 'application/json'
        if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":POST insertData  - "+" PID:"+str(os.getpid()));
        return response  
    
    
@app.route("/workflow/<runid>", methods=['GET', 'DELETE'])
def workflowInfoHandler(runid):
        response=None
        if request.method == 'GET':
            response = Response(json.dumps(app.db.getRunInfo(runid)))
        
        elif request.method == 'DELETE' :
             if (len(runid)<=40):
             
                  response = Response(self.provenanceStore.deleteRun(runid))
             else: 
                  response = {'success':False, 'error':'Invalid Run Id'}
            
                  if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":DELETE WorkflowRunInfo - "+self.path+" PID:"+str(os.getpid()));
        response.headers['Content-type'] = 'application/json'   
        return response


@app.route("/workflow/summaries")
def summariesHandler():
        
        
        #if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":GET getSummaries - level="+request.args['level']);
        response = Response(json.dumps(app.db.getActivitiesSummaries(**request.args)))
        response.headers['Content-type'] = 'application/json'    
        return response

@app.route("/wasDerivedFrom/<id>")
def wasDerivedFrom(id):
    level = request.args['level']
    if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":GET wasDerivedFrom - "+id+" PID:"+str(os.getpid()));
    response = Response(json.dumps(app.db.getTrace(id,int(level))))
    response.headers['Content-type'] = 'application/json'       
    return response

@app.route("/derivedData/<id>")    
def derivedData(id):
    level = request.args['level']
    if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":GET derivedData - "+id+" PID:"+str(os.getpid()));
    response = Response(json.dumps(app.db.getDerivedDataTrace(id,int(level))))
    response.headers['Content-type'] = 'application/json'       
    return response



# the <method> can indicate value-range, hasAncherstorWith or the id of the resource
@app.route("/entities/<method>", methods=['GET','POST'])
def getEntitiesByMethod(method):
        keylist = None
        vluelist= None
        mxvaluelist= None
        mnvaluelist= None
        idlist=None
        response = Response()

        if request.method == 'POST':
            try:
                memory_file = StringIO.StringIO(request.form['ids']);
                idlist = csv.reader(memory_file).next()
                memory_file = StringIO.StringIO(request.form['keys']);
                keylist = csv.reader(memory_file).next()
            #if (self.path=="values-range"):
                memory_file = StringIO.StringIO(request.form['maxvalues']) if 'maxvalues' in request.form else None
                mxvaluelist = csv.reader(memory_file).next()
                memory_file2 = StringIO.StringIO(request.form['minvalues']) if 'minvalues' in request.form else None
                mnvaluelist = csv.reader(memory_file2).next()
                memory_file2 = StringIO.StringIO(request.form['values']) if 'values' in request.form else None
                vluelist = csv.reader(memory_file2).next()
                dataid =StringIO.StringIO(request.form['dataid']) if 'dataid' in request.form else None
        
            except Exception, err:
                None
        else:
         
            try:
                memory_file = StringIO.StringIO(request.args['keys']);
                keylist = csv.reader(memory_file).next()
            #if (self.path=="values-range"):
                memory_file = StringIO.StringIO(request.args['maxvalues']) if 'maxvalues' in request.args else None
                mxvaluelist = csv.reader(memory_file).next()
                memory_file2 = StringIO.StringIO(request.args['minvalues']) if 'minvalues' in request.args else None
                mnvaluelist = csv.reader(memory_file2).next()
                memory_file2 = StringIO.StringIO(request.args['values']) if 'values' in request.args else None
                vluelist = csv.reader(memory_file2).next()
                dataid =StringIO.StringIO(request.args['dataid']) if 'dataid' in request.args else None
            except Exception, err:
                None
        
        
    
        # BEGIN kept for backwards compatibility
        
        if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":GET generatedBy - "+" PID:"+str(os.getpid()));
        ' test http://localhost:8082/entities/hasAnchestor?dataId=lxa88-9865-09df5b44-8f1c-11e3-9f3a-bcaec52d20a2&keys=magnitude&values=3.49&_dc=&page=1&start=0&limit=300'        
        
       # if (self.path=="hasAncestorWith"):
        #    response = Response(json.dumps(self.provenanceStore.hasAncestorWith(dataid,keylist,valuelist)))
        # END kept for backwards compatibility
        
        if (method=="hasAncestorWith"):
            response = Response(json.dumps(app.db.hasAncestorWith(dataid,keylist,valuelist)))
        elif (method=="filterOnAncestorsValuesRange"):
            response = Response(json.dumps(app.db.filterOnAncestorsValuesRange(idlist,keylist,mnvaluelist,mxvaluelist)))
        else:
            response = Response(json.dumps(app.db.getEntitiesBy(method,keylist,mxvaluelist,mnvaluelist,vluelist,**request.args)))
        response.headers['Content-type'] = 'application/json'       
        return response
    
@app.route("/workflow/export/<runid>")
def exportRunProvenance(runid):
 
        if 'all' in request.args and request.args['all'].upper()=='"True"':
            if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":GET exportAllTraces - "+runid+" PID:"+str(os.getpid()));
        
        out,count=app.db.exportRunProvenance(runid,**request.args)
        response=Response(out)
            
        if 'format' in request.args and (request.args['format']=='w3c-prov-xml' or request.args['format']=='w3c-prov-json'):
            response.headers['Content-type']= 'application/octet-stream'#   
                 
        elif 'format' in request.args and request.args['format']=='png':
            response.headers['Content-type']= 'image/png'
                
        else:
            response.headers['Content-type']= 'application/octet-stream'
            
        return response
        #return NOT_DONE_YET
   

@app.route("/workflow/export/data/<id>")
def exportDataProvenance(id):
        if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":GET exportDataTraces - "+id+" PID:"+str(os.getpid()));
        
        out,count=app.db.exportDataProvenance(id,**request.args)
        response=Response(out) 
        
        if 'format' in request.args and (request.args['format']=='w3c-prov-xml' or request.args['format'][0]=='w3c-prov-json'):
            response.headers['Content-type']='application/octet-stream'   
                 
        elif 'format' in request.args and request.args['format']=='png':
            response.headers['Content-type']='image/png'
                
        else:
            response.headers['Content-type']='application/octet-stream'
            
        return response             


' new methods: '

@app.route("/workflowexecution/<runid>/invocations")
def getInvovocationsMonitoring(runid):
    limit = request.args['limit'] 
    start = request.args['start']
    if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET invocations - "+runid+" PID:"+str(os.getpid()));
    response = Response()
    response = Response(json.dumps(app.db.getMonitoring(runid,'invocation',int(start),int(limit))))
    response.headers['Content-type'] = 'application/json'    
    return response

@app.route("/workflowexecution/<runid>/instances")
def getInstancesMonitoring(runid):
    limit = request.args['limit'] 
    start = request.args['start']
     
    if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET instances - "+runid+" PID:"+str(os.getpid()));
    response = Response()
    response = Response(json.dumps(app.db.getMonitoring(runid,'instance',int(start),int(limit))))
    response.headers['Content-type'] = 'application/json'    
    return response

#@app.route("/workflowexecution/<runid>/invocations/<invocid>")
def getInvocationDetails(runid,invocid):
        if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET invocation details - "+invocid+" PID:"+str(os.getpid()));
        response = Response()
        response = Response(json.dumps(app.db.getInvocation(runid,invocid)))
        response.headers['Content-type'] = 'application/json'       
        return response

@app.route("/instances/<instid>")
def getInstanceDetails(runid,instid):
        if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET instance details - "+instid+" PID:"+str(os.getpid()));
        response = Response()
        response = Response(json.dumps(app.db.getComponentInstance(instid)))
        response.headers['Content-type'] = 'application/json'       
        return response


@app.route("/data")
def getData():
        limit = request.args['limit'] 
        start = request.args['start']
        if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET data collection - PID:"+str(os.getpid()));
        
        genby = request.args['generatedBy'] if 'generatedBy' in request.args else None
        attrTo = request.args['attributedTo'] if 'attributedTo' in request.args else None
        keylist = csv.reader(StringIO.StringIO(request.args['keys'])).next() if 'keys' in request.args else None
        maxvalues = csv.reader(StringIO.StringIO(request.args['maxvalues'])) if 'maxvalues' in request.args else None
        minvalues = csv.reader(StringIO.StringIO(request.args['minvalues'])) if 'minvalues' in request.args else None

        
        response = Response(json.dumps(app.db.getData(int(start),int(limit),genBy=genby,attrTo=attrTo,keylist=keylist,maxvalues=maxvalues,minvalues=minvalues)))

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
    