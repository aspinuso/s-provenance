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
app = Flask(__name__)
app.config['DEBUG'] = True
provStore = provenance.ProvenanceStore("mongodb://127.0.0.1/verce-prov")
logging=True
 

@app.route("/")
def hello():
    return "This is the s-prov service"

@app.route("/activities/<runId>")
def activitiesHandler(runId):
    limit = request.args['limit'] 
    start = request.args['start']
     
    #if logging == True : log.msg(str(datetime.datetime.now().time())+":GET activities - "+runId);
    #time.sleep(10)
    #response = Response()
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
             
            if logging == True : log.msg(str(datetime.datetime.now().time())+":GET getUserRuns - "+user);
            response = Response(json.dumps(provStore.getUserRuns(user,**request.args)))
            response.headers['Content-type'] = 'application/json'
            return response
        else:
             
            if logging == True : log.msg(str(datetime.datetime.now().time())+":GET getUserRunsValuesRange - "+user);
            response = Response(json.dumps(provStore.getUserRunsValuesRange(user,keylist,mxvaluelist,mnvaluelist,**request.args)))
            response.headers['Content-type'] = 'application/json'
            return response
        

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
        
        
        #if logging == True : log.msg(str(datetime.datetime.now().time())+":GET getSummaries - level="+request.args['level']);
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



# the <method> can indicate value-range, hasAncherstorWith or the id of the resource
@app.route("/entities/<method>")
def getEntitiesByMethod(method):
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
            dataid =StringIO.StringIO(request.args['dataid']) if 'dataid' in request.args else None
        except Exception, err:
             None
        
        
    
        # BEGIN kept for backwards compatibility
        
        if logging == True : log.msg(str(datetime.datetime.now().time())+":GET generatedBy - ");
        ' test http://localhost:8082/entities/hasAnchestor?dataId=lxa88-9865-09df5b44-8f1c-11e3-9f3a-bcaec52d20a2&keys=magnitude&values=3.49&_dc=&page=1&start=0&limit=300'        
        
       # if (self.path=="hasAncestorWith"):
        #    response = Response(json.dumps(self.provenanceStore.hasAncestorWith(dataid,keylist,valuelist)))
        # END kept for backwards compatibility
        
        if (method=="hasAncestorWith"):
            response = Response(json.dumps(provStore.hasAncestorWith(dataid,keylist,valuelist)))
        else:
            response = Response(json.dumps(provStore.getEntitiesBy(method,keylist,mxvaluelist,mnvaluelist,vluelist,**request.args)))
        response.headers['Content-type'] = 'application/json'       
        return response
    
@app.route("/workflow/export/<runid>")
def exportRunProvenance(runid):
 
        if 'all' in request.args and request.args['all'].upper()=='TRUE':
            if logging == True : log.msg(str(datetime.datetime.now().time())+":GET exportAllTraces - "+runid);
        
        out,count=provStore.exportRunProvenance(runid,**request.args)
        response=Response(json.dumps(out))
            
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
        if logging == True : log.msg(str(datetime.datetime.now().time())+":GET exportDataTraces - "+id);
        
        out,count=provStore.exportDataProvenance(id,**request.args)
        response=Response(json.dumps(out))  
        
        if 'format' in request.args and (request.args['format']=='w3c-prov-xml' or request.args['format'][0]=='w3c-prov-json'):
            response.headers['Content-type']='application/octet-stream'   
                 
        elif 'format' in request.args and request.args['format']=='png':
            response.headers['Content-type']='image/png'
                
        else:
            response.headers['Content-type']='application/octet-stream'
            
        return response             
        
 
if __name__ == "__main__":
    import sys
    #provStore = provenance.ProvenanceStore("mongodb://127.0.0.1/verce-prov")
    logging=False;
    try:
        if (True):
            logging=True
            print("Logging to webserver.out")
            log.startLogging(open("webserver.out", 'a'))
        else:
            logging=True
            print("Logging to stdout")
            log.startLogging(sys.stdout)
    except:
       logging=False
    
    app.run()
    #log.msg("Server running....")
    