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

import time
@app.route("/wasDerivedFrom/<id>")
def wasDerivedFrom(id):
    level = request.args['level']
    if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":GET wasDerivedFrom - "+id+" PID:"+str(os.getpid()));
    app.db.count=0

    

    start_time = time.time()

    result=app.db.getTrace(id,int(level))
    #elapsed_time = time.time() - start_time
    #print(app.db.count)
    #print("ETIME "+str(elapsed_time))
    result=app.db.addLDContext(result[0])
    response = Response(json.dumps(result))
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
@app.route("/data/filterOnAncestor", methods=['GET','POST'])
def getEntitiesByMethod():
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
                memory_file = StringIO.StringIO(request.form['terms']);
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
        
        if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":GET filterOnAncestor PID:"+str(os.getpid()));
        ' test http://localhost:8082/entities/hasAnchestor?dataId=lxa88-9865-09df5b44-8f1c-11e3-9f3a-bcaec52d20a2&keys=magnitude&values=3.49&_dc=&page=1&start=0&limit=300'        
        
       # if (self.path=="hasAncestorWith"):
        #    response = Response(json.dumps(self.provenanceStore.hasAncestorWith(dataid,keylist,valuelist)))
        # END kept for backwards compatibility
        
        #if (method=="hasAncestorWith"):
        #    response = Response(json.dumps(app.db.hasAncestorWith(dataid,keylist,valuelist)))
        #elif (method=="filterOnAncestor"):
        response = Response(json.dumps(app.db.filterOnAncestorsValuesRange(idlist,keylist,mnvaluelist,mxvaluelist)))
        #else:
        #response = Response(json.dumps(app.db.getEntitiesBy(method,keylist,mxvaluelist,mnvaluelist,vluelist,**request.args)))
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


 
# Thomas
# Insert sequences of provenance documents, these can be bundles or lineage. The documents can be in JSON or JSON-LD. Format adaptation for storage purposes is handled by the acquisition function.
@app.route("/workflowexecutions/insert", methods=['POST'])
def insertProvenance():
        
        #print("DADADA "+str(request.get_data()))
         
        payload = request.form["prov"] if "prov" in request.form else request.content.read()
        payload = json.loads(str(payload))
        response = Response(json.dumps(app.db.insertData(payload)))
        response.headers['Content-type'] = 'application/json'
        if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":POST insert provenance  - "+" PID:"+str(os.getpid()));
        return response     


#Update of the user's description of a provenance bundle document. This allow users to explore and improve the description of a run depending from their findings.
@app.route("/workflowexecutions/<runid>/edit", methods=['POST'])
def wfExecDescriptionEdit(runid):
        
        #if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":POST WorkflowRunInfo - "+runid);
        print(request.form)
        response = Response(json.dumps(app.db.editRun(runid,json.loads(str(request.form["doc"])))))
        response.headers['Content-type'] = 'application/json'
        return response

#Deletes the bundle and all the lineage documents related to the \emph{run\_id}.
@app.route("/workflowexecutions/<runid>/delete", methods=['POST'])
def deleteWorkflowRun(runid):
         
        if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":POST workflowexecution delete - "+runid+" PID:"+str(os.getpid()));
        print(request.form)
        response = Response(json.dumps(app.db.deleteRun(runid)))
        response.headers['Content-type'] = 'application/json'
        return response


#Extract documents from the bundle collection by the \id{run\_id} of a \emph{WFExecution} 
@app.route("/workflowexecutions/<runid>", methods=['GET', 'DELETE'])
def getWorkflowInfo(runid):
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

# Thomas
#Extract documents from the bundle collection according to a query string which may include \id{username}, \id{type} of the workflow, its \id{functionNames} and domain metadata \id{terms} and \emph{value-ranges}. 
@app.route("/workflowexecutions")
def getWorkflowExecutions():
    # Required parameters
    limit = request.args['limit'] 
    start = request.args['start']
    usernames = csv.reader(StringIO.StringIO(request.args['usernames'])).next() if 'usernames' in request.args else None

    # include components parameters
    keylist = csv.reader(StringIO.StringIO(request.args['terms'])).next() if ('terms' in request.args and request.args['terms']!="") else None
    maxvalues = csv.reader(StringIO.StringIO(request.args['maxvalues'])).next() if ('maxvalues' in request.args and request.args['maxvalues']!="") else None
    minvalues = csv.reader(StringIO.StringIO(request.args['minvalues'])).next() if ('minvalues' in request.args and request.args['minvalues']!="") else None
    wasAssociatedWith = csv.reader(StringIO.StringIO(request.args['wasAssociatedWith'])).next() if 'wasAssociatedWith' in request.args else None
    implementations = csv.reader(StringIO.StringIO(request.args['implementations'])).next() if 'implementations' in request.args else None
    
    formats = csv.reader(StringIO.StringIO(request.args['formats'])).next() if ('formats' in request.args and request.args['formats']!="") else None
    types = csv.reader(StringIO.StringIO(request.args['types'])).next() if 'types' in request.args else None
    mode = request.args['mode'] if 'mode' in request.args else 'OR'

    # type = csv.reader(StringIO.StringIO(request.args['type'])) if 'type' in request.args else None

    if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET workflowexecutions -  PID:"+str(os.getpid()));
    response = Response()
    # chec functions above in root "/workflow/user/<user>""

    
    if keylist == None and implementations == None and formats==None and usernames!=None:
        response = Response(json.dumps(app.db.getWorkflowExecution(int(start),int(limit),usernames=usernames)))
    else: 
        response = Response(json.dumps(app.db.getWorkflowExecutionByLineage(int(start),int(limit),usernames=usernames, associatedWith=wasAssociatedWith, implementations=implementations, keylist=keylist,maxvalues=maxvalues,minvalues=minvalues, mode=mode, formats=formats)))

    response.headers['Content-type'] = 'application/json'    
    return response


#Extract information about the invocation or instances related to specified \emph{WFExecution} (\id{run\_id}), such as \emph{lastEventTime}, runtime \emph{messages}, indication on the generation of data, its accessibility and its total count. Such a result-set can be used for runtime monitoring, showing progress, data availability and anomalies. Details about a single invocation or  an instance can also be accessed by specifying its $id$. 
@app.route("/workflowexecutions/<runid>/instances")
def getInstancesMonitoring(runid):
    limit = request.args['limit'] 
    start = request.args['start']
    if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET workflowexecutions instances - "+runid+" PID:"+str(os.getpid()));
    response = Response()
    response = Response(json.dumps(app.db.getMonitoring(runid,'instance',int(start),int(limit))))
    response.headers['Content-type'] = 'application/json'    
    return response

@app.route("/workflowexecutions/<runid>/showactivity")
def getMonitoring(runid):
    limit = request.args['limit'] 
    start = request.args['start']
    level = request.args['level'] if 'level' in request.args else None
    if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET workflowexecutions monitoring - "+runid+" PID:"+str(os.getpid()));
    response = Response()
    response = Response(json.dumps(app.db.getMonitoring(runid,level,int(start),int(limit))))
    response.headers['Content-type'] = 'application/json'    
    return response

#Extract details about a single invocation or an instance by specifying their $id$.
@app.route("/invocations/<invocid>")
def getInvocationDetails(invocid):
        
        if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET invocation details - "+invocid+" PID:"+str(os.getpid()));
        response = Response()
        response = Response(json.dumps(app.db.getInvocation(invocid)))
        response.headers['Content-type'] = 'application/json'       
        return response


#Extract details about a single invocation or an instance by specifying their $id$.
@app.route("/instances/<instid>")
def getInstanceDetails(instid): 
        limit = int(request.args['limit']) if 'limit' in request.args else None
        start = int(request.args['start']) if 'start' in request.args else None
        runIds = csv.reader(StringIO.StringIO(request.args['wasAssociateFor'])).next() if 'wasAssociateFor' in request.args else None
        if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET instance details - "+instid+" PID:"+str(os.getpid()));
        response = Response()
        response = Response(json.dumps(app.db.getComponentInstance(instid,runIds=wasAssociateFor,start=start,limit=limit)))
        response.headers['Content-type'] = 'application/json'       
        return response

@app.route("/components/<compid>")
def getComponentDetails(compid):
        if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET component details - "+compid+" PID:"+str(os.getpid()));
        response = Response()
        response = Response(json.dumps(app.db.getComponent(compid)))
        response.headers['Content-type'] = 'application/json'       
        return response


@app.route("/data/<data_id>")
def getDataItem(data_id): 
       
    response = Response(json.dumps(app.db.getData(0,1,id=str(data_id))))
    response.headers['Content-type'] = 'application/json'       
    return response

# Thomas
#The data is selected by specifying its id or a $query\_string$. Query parameters allow to search by \emph{attribution}, \emph{generation} and by combining more metadata terms with their \emph{value-ranges}. Attribution will match all entities of the S-PROV model such as \emph{ComponentInstances}, \emph{Components}, \emph{prov:Person},  while generation will consider \emph{Invocation} and \emph{WorkflowExecution}.
@app.route("/data")
def getData():
        limit = request.args['limit'] 
        start = request.args['start']
        if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET data collection - PID:"+str(os.getpid()));
        #run
        genby = request.args['wasGeneratedBy'] if 'wasGeneratedBy' in request.args else None
        #component
        attrTo = request.args['wasAttributedTo'] if 'wasAttributedTo' in request.args else None
        #implementation
        implementations = request.args['implementations'] if 'implementations' in request.args else None
        keylist = csv.reader(StringIO.StringIO(request.args['terms'])).next() if 'terms' in request.args else None
        maxvalues = csv.reader(StringIO.StringIO(request.args['maxvalues'])).next() if 'maxvalues' in request.args else None
        minvalues = csv.reader(StringIO.StringIO(request.args['minvalues'])).next() if 'minvalues' in request.args else None
        format = request.args['format'] if 'format' in request.args else None
        mode = request.args['mode'] if 'mode' in request.args else 'OR'
        id = request.args['id'] if 'id' in request.args else None
        
        response = Response(json.dumps(app.db.getData(int(start),int(limit),impl=implementations,genBy=genby,attrTo=attrTo,keylist=keylist,maxvalues=maxvalues,minvalues=minvalues,id=id,format=format,mode=mode)))

        response.headers['Content-type'] = 'application/json'

        return response






# Thomas
#@app.route("data/<data_id>/hasAncestorWith")

# Thomas
#Returns a list of metadata terms that can be suggested based on their appearance within a list of runs, users, or for the whole provenance archive
@app.route("/terms")
def getDataGranuleTerms():
        aggregationLevel = request.args['aggregationLevel'] if 'aggregationLevel' in request.args else 'all'
        runIdList = csv.reader(StringIO.StringIO(request.args['runIds'])).next() if 'runIds' in request.args else None
        usernameList = csv.reader(StringIO.StringIO(request.args['usernames'])).next() if 'usernames' in request.args else None
        print('----->', aggregationLevel, runIdList, usernameList)
        
        respjson={}
        data = app.db.getDataGranuleTerms(aggregationLevel=aggregationLevel,runIdList=runIdList,usernameList=usernameList)
        respjson["metadata"]=data["_id"]
        respjson["terms"]=[]
         
        for x in data["value"]["contentMap"]:
            respjson["terms"].append({"term":x,"use":"metadata","valuesByType":data["value"]["contentMap"][x]["valuesByType"]})

        for x in data["value"]["parameterMap"]:
            respjson["terms"].append({"term":x,"use":"parameter","valuesByType":data["value"]["parameterMap"][x]["valuesByType"]})


        response = Response(json.dumps(respjson))

        response.headers['Content-type'] = 'application/json'



        return response


@app.route("/summaries/workflowexecution")
def summariesHandlerWorkflow():
        if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+": GET getSummaries workflow - level= "+request.args['level']);
        
        # the db function can be split in two to serve worklfow executions and collaborative views with explicit parameters
        response = Response(json.dumps(app.db.getActivitiesSummaries(**request.args)))
        response.headers['Content-type'] = 'application/json'    
        return response

# Thomas check value-range level
# Extract information about the reuse and exchange of data between workflow executions, users and infrastructures, based terms and values' ranges. These Additional properties, such as workflow's type or (\id{prov:type})  can be also extracted
@app.route("/summaries/collaborative")
def summariesHandlerCollab():
        users = csv.reader(StringIO.StringIO(request.args['users'])).next() if 'users' in request.args else None
        groupby = request.args['groupby'] if 'groupby' in request.args else None
        mode = request.args['mode']if 'mode' in request.args else None
        keylist = csv.reader(StringIO.StringIO(request.args['terms'])).next() if 'terms' in request.args else None
        maxvalues = csv.reader(StringIO.StringIO(request.args['maxvalues'])).next() if 'maxvalues' in request.args else None
        minvalues = csv.reader(StringIO.StringIO(request.args['minvalues'])).next() if 'minvalues' in request.args else None

        print(minvalues)
        

        if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+": GET getSummaries collab - level= "+request.args['level']);

        # the db function can be split in two to serve worklfow executions and collaborative views with explicit parameters as follows
        #app.db.getCollaboariveSummaries(users=users,groupby=groupby,mode=mode,keylist=keylist,maxvalues=maxvalues,minvalues=minvalues)))

        #in that case level would not be needed anymore if we split the db function in two
        level = csv.reader(StringIO.StringIO(request.args['level'])).next() if 'level' in request.args else None

        
        #response = Response(json.dumps(app.db.getActivitiesSummaries(**request.args)))
        response = Response(json.dumps(app.db.getCollaborativeSummariesWorkfows(mode=mode,groupby=groupby,users=users,keylist=keylist,maxvalues=maxvalues,minvalues=minvalues)))
        
        response.headers['Content-type'] = 'application/json'    
        return response

#Thomas
#@app.route("data/<data_id>/derivedData")

#Thomas
#@app.route("data/<data_id>/wasDerivedFrom")


# EXPORT to PROV methods
@app.route("/data/<data_id>/export")
def _exportDataProvenance(data_id):
    return exportDataProvenance(data_id)


@app.route("/workflowexecutions/<run_id>/export")
def _exportRunProvenance(run_id):
    return exportRunProvenance(run_id)


if __name__ == "__main__":
    import sys
    #app.db = provenance.ProvenanceStore("mongodb://127.0.0.1/verce-prov")
    logging=False;
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(stream_handler)
    app.run()
    # app.logger.info("Server running....")
    
