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
    
    limit = request.args['limit'] 
    start = request.args['start']
   
    #if logging == True : log.msg(str(datetime.datetime.now().time())+":GET activities - "+runId);
    response = Response(json.dumps(provStore.getActivities(runId,int(start),int(limit))))
    response.headers['Content-type'] = 'application/json'    
    return response


@app.route("/workflow")
def workflowsHandler(runid):
        
        response = Response(json.dumps(provStore.getWorkflows(**request.args)))
        response.headers['Content-type'] = 'application/json'
        return response
    
@app.route("/workflow/user/<user>")  
def getUserRuns(user):
        
        keylist = None
        vluelist= None
        mxvaluelist= None
        mnvaluelist= None
       
        limit = request.args['limit'][0]
        start = request.args['start'][0]
       
         
        try:
            memory_file = StringIO.StringIO(request.args['keys'][0]);
            keylist = csv.reader(memory_file).next()
            
            memory_file = StringIO.StringIO(request.args['maxvalues'][0]);
            mxvaluelist = csv.reader(memory_file).next()
            memory_file = StringIO.StringIO(request.args['minvalues'][0]);
            mnvaluelist = csv.reader(memory_file).next()
        
        except Exception, err:
            None
            
         
        if (keylist==None and 'activities' not in request.args):
            print("A")
            if logging == True : log.msg(str(datetime.datetime.now().time())+":GET getUserRuns - "+user);
            response = Response(json.dumps(provStore.getUserRuns(user,**request.args)))
            response.headers['Content-type'] = 'application/json'
            return response
        else:
            print("B")
            if logging == True : log.msg(str(datetime.datetime.now().time())+":GET getUserRunsValuesRange - "+self.path);
            response = Response(provStore.getUserRunsValuesRange(user,keylist,mxvaluelist,mnvaluelist,**request.args))
            response.headers['Content-type'] = 'application/json'
            return json.dumps(response)
        

@app.route("/workflow/edit/<runid>", methods=['POST'])
def workflowInfoHandlerEdit(runid):
        
        #if logging == True : log.msg(str(datetime.datetime.now().time())+":POST WorkflowRunInfo - "+runid);
        print(request.form)
        response = Response(json.dumps(provStore.editRun(runid,json.loads(str(request.form["doc"])))))
        response.headers['Content-type'] = 'application/json'
        return response
    

@app.route("/workflow/delete/<runid>", methods=['POST'])
def workflowInfoHandlerDelete(runid):
         
        if logging == True : log.msg(str(datetime.datetime.now().time())+":POST WorkflowRunInfo - "+runid);
        print(request.form)
        response = Response(json.dumps(provStore.deleteRun(runid)))
        response.headers['Content-type'] = 'application/json'
        return response

@app.route("/workflow/insert", methods=['POST'])
def insertData():
        payload = request.form["prov"] if "prov" in request.form else request.content.read()
        payload = json.loads(str(payload))
        response = Response(json.dumps(provStore.insertData(payload)))
        response.headers['Content-type'] = 'application/json'
        if logging == True : log.msg(str(datetime.datetime.now().time())+":POST insertData  - ")
        return response  
    
    
@app.route("/workflow/<runid>", methods=['GET', 'DELETE'])
def workflowInfoHandler(runid):
        response=None
        if request.method == 'GET':
            response = Response(json.dumps(provStore.getRunInfo(runid)))
        
        elif request.method == 'DELETE' :
             if (len(runid)<=40):
             
                  response = Response(self.provenanceStore.deleteRun(runid))
             else: 
                  response = {'success':False, 'error':'Invalid Run Id'}
            
                  if logging == True : log.msg(str(datetime.datetime.now().time())+":DELETE WorkflowRunInfo - "+self.path);
        response.headers['Content-type'] = 'application/json'   
        return response


@app.route("/workflow/summaries")
def summariesHandler():
        
        
        #if logging == True : log.msg(str(datetime.datetime.now().time())+":GET getSummaries - level="+request.args['level'][0]);
        response = Response(json.dumps(provStore.getActivitiesSummaries(**request.args)))
        response.headers['Content-type'] = 'application/json'    
        return response

@app.route("/wasDerivedFrom/<id>")
def wasDerivedFrom(id):
    level = request.args['level']
    if logging == True : log.msg(str(datetime.datetime.now().time())+":GET wasDerivedFrom - "+id);
    response = Response(json.dumps(provStore.getTrace(id,int(level))))
    response.headers['Content-type'] = 'application/json'       
    return response

@app.route("/derivedData/<id>")    
def derivedData(id):
    level = request.args['level']
    if logging == True : log.msg(str(datetime.datetime.now().time())+":GET derivedData - "+id);
    response = Response(json.dumps(provStore.getDerivedDataTrace(id,int(level))))
    response.headers['Content-type'] = 'application/json'       
    return response

@app.route("/entities/generatedby")
def generatedBy():
        keylist = None
        vluelist= None
        mxvaluelist= None
        mnvaluelist= None
        
        response = Response()
        
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
        
        except Exception, err:
            None
        
        
    
        # BEGIN kept for backwards compatibility
        if logging == True : log.msg(str(datetime.datetime.now().time())+":GET generatedBy - ");
        ' test http://localhost:8082/entities/hasAnchestor?dataId=lxa88-9865-09df5b44-8f1c-11e3-9f3a-bcaec52d20a2&keys=magnitude&values=3.49&_dc=&page=1&start=0&limit=300'        
        
       # if (self.path=="hasAncestorWith"):
        #    response = Response(json.dumps(self.provenanceStore.hasAncestorWith(dataid,keylist,valuelist)))
        # END kept for backwards compatibility
        
        
        response = Response(json.dumps(provStore.getEntitiesBy("generatedby",keylist,mxvaluelist,mnvaluelist,vluelist,**request.args)))
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
    
    app.run(debug=True,threaded=True,port=8082)
    #log.msg("Server running....")
    