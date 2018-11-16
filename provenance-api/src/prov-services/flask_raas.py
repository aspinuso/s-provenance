import provenance as provenance
import json
import webargs
import csv
import StringIO
import traceback
import datetime
from prov.model import ProvDocument, Namespace, Literal, PROV, Identifier
from flask import Flask
from flask import request
from flask import Response
from flask_cors import CORS

import logging
import sys
import os

from flask_apispec import use_kwargs, marshal_with, doc, FlaskApiSpec
from marshmallow import fields, Schema


app = Flask(__name__)
app.config['DEBUG'] = True
logging=os.environ['RAAS_LOGGING']
CORS(app)

class PetSchema(Schema):
    class Meta:
        fields = ('name', 'category', 'size')


def bootstrap_app():
    app.db=provenance.ProvenanceStore(os.environ['RAAS_REPO'])
    return app

@app.route("/")
def hello():
    return "This is the s-prov service"




    

 
# Thomas
# Insert sequences of provenance documents, these can be bundles or lineage. The documents can be in JSON or JSON-LD. Format adaptation for storage purposes is handled by the acquisition function.
@app.route("/workflowexecutions/insert", methods=['POST'])
@use_kwargs({'prov': fields.Str()})
@doc(tags=['acquisition'], description='Bulk insert of bundle or lineage documents in JSON format. These must be provided as encoded stirng in a POST request')
def insert_provenance(**kwargs):
        
         
        payload = kwargs["prov"] if "prov" in kwargs else request.content.read()
        payload = json.loads(str(payload))
        response = Response(json.dumps(app.db.insertData(payload)))
        response.headers['Content-type'] = 'application/json'
        if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":POST insert provenance  - "+" PID:"+str(os.getpid()));
        return response     


#Update of the user's description of a provenance bundle document. This allow users to explore and improve the description of a run depending from their findings.
@app.route("/workflowexecutions/<runid>/edit", methods=['POST'])
@use_kwargs({'doc': fields.Str(required=True)})
@doc(tags=['acquisition'], description='Update of the description of a workflow execution. Users can improve this information in free-tex')
def wfexec_description_edit(runid,**kwargs):
        
        #if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":POST WorkflowRunInfo - "+runid);
        payload = kwargs["doc"]
        response = Response(json.dumps(app.db.editRun(runid,json.loads(str(payload)))))
        response.headers['Content-type'] = 'application/json'
        return response

#Deletes the bundle and all the lineage documents related to the \emph{run\_id}.

@app.route("/workflowexecutions/<runid>/delete", methods=['POST'])
@doc(tags=['acquisition'], description='Delete a workflow execution trace, including its bundle and all its lineage documents')
def delete_workflow_run(runid):
         
        if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":POST workflowexecution delete - "+runid+" PID:"+str(os.getpid()));
        response = Response(json.dumps(app.db.deleteRun(runid)))
        response.headers['Content-type'] = 'application/json'
        return response


#Extract documents from the bundle collection by the \id{run\_id} of a \emph{WFExecution} 


paging ={ 'start': fields.Int(required=True),
          'limit': fields.Int(required=True)
          }

 
queryargsbasic = {
             'terms': fields.Str(),
             'maxvalues': fields.Str(),
             'minvalues': fields.Str(),
             'wasAssociatedWith': fields.Str(),
             'mode': fields.Str(),
             'rformat': fields.Str(missing="json")
              }

queryargsnp = {'usernames': fields.Str(),
             'terms': fields.Str(),
             'maxvalues': fields.Str(),
             'minvalues': fields.Str(),
             'wasAssociatedWith': fields.Str(),
             'functionNames' : fields.Str(),
             'clusters' : fields.Str(),
             'types': fields.Str(),
             'mode': fields.Str(),
             'formats': fields.Str(),
             'rformat': fields.Str(missing="json")
              }


queryargsnpdata = {'usernames': fields.Str(),
             'terms': fields.Str(),
             'maxvalues': fields.Str(),
             'minvalues': fields.Str(),
             'functionNames' : fields.Str(),
             'clusters' : fields.Str(),
             'types': fields.Str(),
             'mode': fields.Str(),
             'formats': fields.Str(),
             'rformat': fields.Str(missing="json")
              }

queryargs =dict(queryargsnp,**paging)

@app.route("/workflowexecutions/<runid>", methods=['GET', 'DELETE'])
@doc(tags=['discovery'], description='Extract documents from the bundle collection by the runid of a WFExecution. The method will return input data and infomation about the components and the libraries used for the specific run')
def get_workflow_info(runid):
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
@use_kwargs(queryargs, locations=["querystring"])
@doc(tags=['discovery'], description='Extract documents from the bundle collection according to a query string which may include usernames, type of the workflow, the components the run wasAssociatedWith and their implementations. Data results\' metadata and parameters can also be queried by specifying the terms and their min and max values-ranges and data formats. Mode of the search can also be indicated (mode ::= (OR j AND). It will apply to the search upon metadata and parameters values of each run')
def get_workflowexecutions(**kwargs):
    # Required parameters
    limit = kwargs['limit'] 
    start = kwargs['start']
    print(limit)
    usernames = csv.reader(StringIO.StringIO(kwargs['usernames'])).next() if 'usernames' in kwargs else None

    # include components parameters
    keylist = csv.reader(StringIO.StringIO(kwargs['terms'])).next() if ('terms' in kwargs and kwargs['terms']!="") else None
    maxvalues = csv.reader(StringIO.StringIO(kwargs['maxvalues'])).next() if ('maxvalues' in kwargs and kwargs['maxvalues']!="") else None
    minvalues = csv.reader(StringIO.StringIO(kwargs['minvalues'])).next() if ('minvalues' in kwargs and kwargs['minvalues']!="") else None
    wasAssociatedWith = csv.reader(StringIO.StringIO(kwargs['wasAssociatedWith'])).next() if 'wasAssociatedWith' in kwargs else None
    implementations = csv.reader(StringIO.StringIO(kwargs['functionNames'])).next() if ('functionNames' in kwargs and kwargs['functionNames']!="") else None
    clusters = csv.reader(StringIO.StringIO(kwargs['clusters'])).next() if ('clusters' in kwargs and kwargs['clusters']!="") else None
    print clusters
    formats = csv.reader(StringIO.StringIO(kwargs['formats'])).next() if ('formats' in kwargs and kwargs['formats']!="" and kwargs['formats']!="null") else None
    types = csv.reader(StringIO.StringIO(kwargs['types'])).next() if ('types' in kwargs and kwargs['types']!="") in kwargs else None
    mode = kwargs['mode'] if 'mode' in kwargs else 'OR'

    # type = csv.reader(StringIO.StringIO(kwargs['type'])) if 'type' in request.args else None

    if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET workflowexecutions -  PID:"+str(os.getpid()));
    response = Response()
    # chec functions above in root "/workflow/user/<user>""

    
    if keylist == None and implementations == None and formats==None and usernames!=None and clusters == None:
        response = Response(json.dumps(app.db.getWorkflowExecution(int(start),int(limit),usernames=usernames)))
    else: 
        response = Response(json.dumps(app.db.getWorkflowExecutionByLineage(int(start),int(limit),usernames=usernames, associatedWith=wasAssociatedWith, implementations=implementations, keylist=keylist,maxvalues=maxvalues,minvalues=minvalues, mode=mode, types=types,formats=formats,clusters=clusters)))

    response.headers['Content-type'] = 'application/json'    
    return response


#Extract information about the invocation or instances related to specified \emph{WFExecution} (\id{run\_id}), such as \emph{lastEventTime}, runtime \emph{messages}, indication on the generation of data, its accessibility and its total count. Such a result-set can be used for runtime monitoring, showing progress, data availability and anomalies. Details about a single invocation or  an instance can also be accessed by specifying its $id$. 
@app.route("/workflowexecutions/<runid>/instances")
@use_kwargs(paging,locations=["querystring"])
def get_instances_monitoring(runid,**kwargs):
    limit = kwargs['limit'] 
    start = kwargs['start']
    if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET workflowexecutions instances - "+runid+" PID:"+str(os.getpid()));
    response = Response()
    response = Response(json.dumps(app.db.getMonitoring(runid,'instance',int(start),int(limit))))
    response.headers['Content-type'] = 'application/json'    
    return response

levelargsnp=dict({"level":fields.Str(required=True)})
levelargs=dict({"level":fields.Str()},**paging)
 
@app.route("/workflowexecutions/<runid>/showactivity")
@use_kwargs(levelargs,locations=["querystring"])
@doc(tags=['monitor'], description='Extract detailed information related to the activity related to a WFExecution (id). The result-set can be grouped by invocations, instances or components (parameter level) and shows progress, anomalies (such as exceptions or systems\' and users messages), occurrence of changes and the rapid availability of accessible data bearing intermediate results. This method can also be used for runtime monitoring')
def get_monitoring(runid,**kwargs):
    limit = kwargs['limit'] 
    start = kwargs['start']
    level = kwargs['level'] if 'level' in kwargs else None
    if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET workflowexecutions monitoring - "+runid+" PID:"+str(os.getpid()));
    response = Response()
    response = Response(json.dumps(app.db.getMonitoring(runid,level,int(start),int(limit))))
    response.headers['Content-type'] = 'application/json'    
    return response

#Extract details about a single invocation or an instance by specifying their $id$.
@app.route("/invocations/<invocid>")
@doc(tags=['lineage'], description='Extract details about a single invocation by specifying its id')
def get_invocation_details(invocid):
        
        if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET invocation details - "+invocid+" PID:"+str(os.getpid()));
        response = Response()
        response = Response(json.dumps(app.db.getInvocation(invocid)))
        response.headers['Content-type'] = 'application/json'       
        return response


#Extract details about a single invocation or an instance by specifying their $id$.
associatefor=dict({"wasAssociateFor":fields.Str()},**paging)
@app.route("/instances/<instid>")
@use_kwargs(associatefor,locations=["querystring"])
@doc(tags=['lineage'], description='Extract details about a single instance or component by specifying its id. The returning document will indicate the changes that occurred, reporting the first invocation affected. It support the specification of a list of runIds the instance was wasAssociateFor, considering that the same instance could be used across multiple runs')
def get_instance_details(instid,**kwargs): 
        limit = int(kwargs['limit']) if 'limit' in kwargs else None
        start = int(kwargs['start']) if 'start' in kwargs else None
        runIds = csv.reader(StringIO.StringIO(kwargs['wasAssociateFor'])).next() if 'wasAssociateFor' in kwargs else None
        if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET instance details - "+instid+" PID:"+str(os.getpid()));
        response = Response()
        response = Response(json.dumps(app.db.getComponentInstance(instid,runIds=runIds,start=start,limit=limit)))
        response.headers['Content-type'] = 'application/json'       
        return response

#instances=dict({"wasAssociateFor":fields.Str()},**paging)
@app.route("/components/<compid>")
@doc(tags=['lineage'], description='Extract details about a single component by specifying its id and the workflow run it wasAssociateFor, considering that the the same components could be used across multiple runs. The returning document will indicate the changes that occurred, reporting the first invocation affected')
@use_kwargs(associatefor,locations=["querystring"])
def getComponentDetails(compid, **kwargs):
        limit = int(kwargs['limit']) if 'limit' in kwargs else None
        start = int(kwargs['start']) if 'start' in kwargs else None
        runIds = csv.reader(StringIO.StringIO(kwargs['wasAssociateFor'])).next() if 'wasAssociateFor' in kwargs else None
        if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET component details - "+compid+" PID:"+str(os.getpid()));
        response = Response()
        response = Response(json.dumps(app.db.getComponent(compid,runIds=runIds,start=start,limit=limit)))
        response.headers['Content-type'] = 'application/json'       
        return response


@app.route("/data/<data_id>")
@doc(tags=['lineage'], description='Extract Data and their DataGranules by the Data id')
def get_data_item(data_id): 
       
    response = Response(json.dumps(app.db.getData(0,1,id=str(data_id))))
    response.headers['Content-type'] = 'application/json'       
    return response

# Thomas
#The data is selected by specifying its id or a $query\_string$. Query parameters allow to search by \emph{attribution}, \emph{generation} and by combining more metadata terms with their \emph{value-ranges}. Attribution will match all entities of the S-PROV model such as \emph{ComponentInstances}, \emph{Components}, \emph{prov:Person},  while generation will consider \emph{Invocation} and \emph{WorkflowExecution}.
dataargs=dict({'wasGeneratedBy':fields.Str(),
               'wasAttributedTo':fields.Str()},**queryargsnpdata)

dataargs =dict(dataargs,**paging)

@app.route("/data",methods=['GET'])
@doc(tags=['lineage'], description='The data is selected by specifying a query string. Query parameters allow to search by attribution to a component or to an implementation, generation by a workflow execution and by combining more metadata and parameters terms with their min and max valuesranges. Mode of the search can also be indicated (mode ::= (OR | AND). It will apply to the search upon metadata and parameters values-ranges')
@use_kwargs(dataargs,locations=["querystring"])
def get_data(**kwargs):
    limit = kwargs['limit'] 
    start = kwargs['start']
    if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET data collection - PID:"+str(os.getpid()));
    #run
    genby = kwargs['wasGeneratedBy'] if 'wasGeneratedBy' in kwargs else None
    #component
    attrTo = kwargs['wasAttributedTo'] if 'wasAttributedTo' in kwargs else None
    #implementation
    implementations = kwargs['functionNames'] if ('functionNames' in kwargs and kwargs['functionNames']!="") else None
    clusters = kwargs['clusters'] if ('clusters' in kwargs and kwargs['clusters']!="") else None
    keylist = csv.reader(StringIO.StringIO(kwargs['terms'])).next() if 'terms' in kwargs else None
    maxvalues = csv.reader(StringIO.StringIO(kwargs['maxvalues'])).next() if 'maxvalues' in kwargs else None
    minvalues = csv.reader(StringIO.StringIO(kwargs['minvalues'])).next() if 'minvalues' in kwargs else None
    format = kwargs['formats'] if 'formats' in kwargs else None
    mode = kwargs['mode'] if 'mode' in kwargs else 'OR'
    #id = kwargs['id'] if 'id' in kwargs else None
    
    response = Response(json.dumps(app.db.getData(int(start),int(limit),impl=implementations,genBy=genby,attrTo=attrTo,keylist=keylist,maxvalues=maxvalues,minvalues=minvalues,id=None,format=format,mode=mode,clusters=clusters)))

    response.headers['Content-type'] = 'application/json'

    return response

#Thomas
@app.route("/data/<data_id>/derivedData")
@use_kwargs(levelargsnp,locations=["querystring"])
@doc(tags=['lineage'], description='Starting from a specific data entity of the data dependency is possible to navigate through the derived data or backwards across the element\'s data dependencies. The number of traversal steps is provided as a parameter (level).')
def derived_data(data_id,**kwargs):
    level = kwargs['level']
    if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":GET derivedData - "+data_id+" PID:"+str(os.getpid()));
    response = Response(json.dumps(app.db.getDerivedDataTrace(data_id,int(level))))
    response.headers['Content-type'] = 'application/json'       
    return response

#Thomas
@app.route("/data/<data_id>/wasDerivedFrom")
@use_kwargs(levelargsnp,locations=["querystring"])
@doc(tags=['lineage'], description='Starting from a specific data entity of the data dependency is possible to navigate through the derived data or backwards across the element\'s data dependencies. The number of traversal steps is provided as a parameter (level).')
def was_derived_from(data_id,**kwargs):
    print(kwargs)
    level = kwargs['level']
    if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":GET wasDerivedFrom - "+data_id+" PID:"+str(os.getpid()));
    app.db.count=0


    

    #start_time = time.time()

    result=app.db.getTrace(data_id,int(level))
    #elapsed_time = time.time() - start_time
    #print(app.db.count)
    #print("ETIME "+str(elapsed_time))
    result=app.db.addLDContext(result[0])
    response = Response(json.dumps(result))
    response.headers['Content-type'] = 'application/json'       
    return response






# Thomas
#@app.route("data/<data_id>/hasAncestorWith")

# Thomas
#Returns a list of metadata terms that can be suggested based on their appearance within a list of runs, users, or for the whole provenance archive
termsargs=dict({'runIds':fields.Str(),
                'usernames':fields.Str(),
                'aggregationLevel':fields.Str()})

@app.route("/terms")
@use_kwargs(termsargs,locations=["querystring"])
@doc(tags=['lineage'], description='Return a list of discoverable metadata terms based on their appearance for a list of runIds, usernames, or for the whole provenance archive. Terms are returned indicating their type (when consistently used), min and max values and their number occurrences within the scope of the search')
def get_data_granule_terms(**kwargs):
        aggregationLevel = kwargs['aggregationLevel'] if 'aggregationLevel' in kwargs else 'all'
        runIdList = csv.reader(StringIO.StringIO(kwargs['runIds'])).next() if 'runIds' in kwargs else None
        usernameList = csv.reader(StringIO.StringIO(kwargs['usernames'])).next() if 'usernames' in kwargs else None
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

summaryargs=dict({'runId':fields.Str(),
                  'groupby':fields.Str(),
                  'clusters':fields.Str(),
                  'mintime':fields.Str(),
                  'maxtime':fields.Str(),
                  'minidx':fields.Int(),
                  'maxidx':fields.Int()

                  },**levelargsnp)

@app.route("/summaries/workflowexecution")
@use_kwargs(summaryargs,locations=["querystring"])
@doc(tags=['summaries'], description='Produce a detailed overview of the distribution of the computation, reporting the size of data movements between the workflow components, their instances or invocations across worker nodes, depending on the specified granularity level. Additional information, such as process pid, worker, instance or component of the workflow (depending on the level of granularity) can be selectively extracted by assigning these properties to a groupBy parameter. This will support the generation of grouped views')
def summaries_handler_workflow(**kwargs):
        if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+": GET getSummaries workflow - level= "+kwargs['level']);
        print kwargs
        # the db function can be split in two to serve worklfow executions and collaborative views with explicit parameters
        response = Response(json.dumps(app.db.getActivitiesSummaries(**kwargs)))
        response.headers['Content-type'] = 'application/json'    
        return response

# Thomas check value-range level
# Extract information about the reuse and exchange of data between workflow executions, users and infrastructures, based terms and values' ranges. These Additional properties, such as workflow's type or (\id{prov:type})  can be also extracted

colargs=dict(dict({'groupby':fields.Str()},**queryargsnp),**levelargsnp)

@app.route("/summaries/collaborative")
@use_kwargs(colargs,locations=["querystring"])
@doc(tags=['summaries'], description='Extract information about the reuse and exchange of data between workflow executions based on terms\' valuesranges and a group of users. The API method allows for inclusive or exclusive (mode ::= (OR j AND) queries on the terms\' values. As above, additional details, such as running infrastructure, type and name of the workflow can be selectively extracted by assigning these properties to a groupBy parameter. This will support the generation of grouped views')
def summaries_handler_collab(**kwargs):
        users = csv.reader(StringIO.StringIO(kwargs['usernames'])).next() if 'usernames' in kwargs else None
        groupby = kwargs['groupby'] if 'groupby' in kwargs else None
        mode = kwargs['mode']if 'mode' in kwargs else None
        keylist = csv.reader(StringIO.StringIO(kwargs['terms'])).next() if 'terms' in kwargs else None
        maxvalues = csv.reader(StringIO.StringIO(kwargs['maxvalues'])).next() if 'maxvalues' in kwargs else None
        minvalues = csv.reader(StringIO.StringIO(kwargs['minvalues'])).next() if 'minvalues' in kwargs else None

        print(minvalues)
        

        if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+": GET getSummaries collab - level= "+kwargs['level']);

        response = Response(json.dumps(app.db.getCollaborativeSummariesWorkfows(mode=mode,groupby=groupby,users=users,keylist=keylist,maxvalues=maxvalues,minvalues=minvalues)))
        
        response.headers['Content-type'] = 'application/json'    
        return response



exportprov=dict({'format':fields.Str(enum=['rdf', 'json','xml','provn']),'rdfout':fields.Str(missing='trig',enum=['xml', 'n3', 'nt', 'trix','trig','turtle']),'creator':fields.Str()})
exportdata=dict(exportprov,**levelargsnp)
# EXPORT to PROV methods

@app.route("/data/<data_id>/export")
@doc(tags=['export'], description='Export of provenance information PROV-XML or RDF format. The S-PROV information returned covers the whole workflow execution or is restricted to a single data element. In the latter case, the graph is returned by following the derivations within and across runs. A level parameter allows to indicate the depth of the resulting trace')
@use_kwargs(exportdata,locations=["querystring"])
def export_data_provenance(data_id,**kwargs):
    
    if 'creator' in kwargs:
      creator = kwargs['creator'] 
      del kwargs['creator']
    else:
      creator =  "anonymous"
     
    response = Response(str(app.db.exportDataProvenance(data_id,creator,**kwargs)).encode('ascii','ignore'))
    if 'format' in kwargs and kwargs['format']=='rdf':
        response.headers['Content-type'] = 'application/turtle' 
    elif 'format' in kwargs and kwargs['format']=='json':
        response.headers['Content-type'] = 'application/json'
    elif 'format' in kwargs and kwargs['format']=='xml':
        response.headers['Content-type'] = 'application/xml' 
    else:
        response.headers['Content-type'] = 'application/octet-streams' 
    return response

queryargsanc=dict(dict({'ids':fields.Str()},**queryargsbasic),**levelargsnp)
@app.route("/data/filterOnAncestor", methods=['POST'])
@use_kwargs(queryargsanc)
@doc(tags=['lineage'], description='Filter a list of data ids based on the existence of at least one ancestor in their data dependency graph, according to a list of metadata terms and their min and max values-ranges. Maximum depth level and mode of the search can also be indicated (mode ::= (OR | AND)')
def filter_on_ancestor(**kwargs):

        keylist = None
        vluelist= None
        mxvaluelist= None
        mnvaluelist= None
        idlist=None
        level=None
       

    
        memory_file = StringIO.StringIO(kwargs['ids']);
        idlist = csv.reader(memory_file).next()
        memory_file = StringIO.StringIO(kwargs['terms']);
        keylist = csv.reader(memory_file).next()

        #if (self.path=="values-range"):
        memory_file = StringIO.StringIO(kwargs['maxvalues']) if 'maxvalues' in kwargs else None
        mxvaluelist = csv.reader(memory_file).next()
        memory_file2 = StringIO.StringIO(kwargs['minvalues']) if 'minvalues' in kwargs else None
        mnvaluelist = csv.reader(memory_file2).next()
        #memory_file2 = StringIO.StringIO(kwargs['values']) if 'values' in kwargs else None
        #vluelist = csv.reader(memory_file2).next()
        #dataid =StringIO.StringIO(kwargs['dataid']) if 'dataid' in kwargs else None
        
        level =int(kwargs['level']) if 'level' in kwargs else 100
        mode = kwargs['mode'] if 'mode' in kwargs else 'OR'

        if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":POST filterOnAncestor mode= "+str(mode)+" PID:"+str(os.getpid()));
        res=json.dumps(app.db.filterOnAncestorsValuesRange(idlist,keylist,mnvaluelist,mxvaluelist,level=level,mode=mode))
        print(res)
        response = Response(res)
        response.headers['Content-type'] = 'application/json'    
        return response





@app.route("/workflowexecutions/<run_id>/export")
@use_kwargs(exportprov,locations=["querystring"])
@doc(tags=['export'], description='Export of provenance information PROV-XML or RDF format. The S-PROV information returned covers the whole workflow execution or is restricted to a single data element. In the latter case, the graph is returned by following the derivations within and across runs. A level parameter allows to indicate the depth of the resulting trace')
def export_run_provenance(run_id,**kwargs):

    
    if 'creator' in kwargs:
      creator = kwargs['creator'] 
      del kwargs['creator']
    else:
      creator =  "anonymous"
    
    response = Response(str(app.db.exportRunProvenance(run_id,creator,**kwargs)).encode('ascii','ignore'))

    if 'format' in kwargs and kwargs['format']=='rdf':
        response.headers['Content-type'] = 'application/turtle' 
    elif 'format' in kwargs and kwargs['format']=='json':
        response.headers['Content-type'] = 'application/json'
    elif 'format' in kwargs and kwargs['format']=='xml':
        response.headers['Content-type'] = 'application/xml' 
    else:
        response.headers['Content-type'] = 'application/octet-streams' 
    return response



@app.errorhandler(422)
def handle_validation_error(err):
    exc = err.exc
    response = Response(json.dumps({'errors': exc.messages}))
    response.headers['Content-type'] = 'application/json'   
    return response





#

 

if __name__ == "__main__":
    import sys
    #app.db = provenance.ProvenanceStore("mongodb://127.0.0.1/verce-prov")
    logging=False;
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(stream_handler)

    
    #app.add_url_rule('/stores', view_func=StoreResource.as_view('Store'))

    app.run()
    # app.logger.info("Server running....")
 
from apispec import APISpec
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='s-prov',
        version='v1',
        plugins=['apispec.ext.marshmallow'],
         schemes=['http','https'],
        description="S-ProvFlow provenance API - Provenance framework for storage and access of data-intensive streaming lineage. It offers a a web API and a range of dedicated visualisation tools and a provenance model (S-PROV) which utilises and extends PROV and ProvONE model"
    
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
    })
docs = FlaskApiSpec(app)


docs.register(insert_provenance)
docs.register(wfexec_description_edit)
docs.register(delete_workflow_run)

docs.register(get_workflow_info)
docs.register(get_workflowexecutions)
#docs.register(get_instances_monitoring)
docs.register(get_monitoring)
docs.register(get_invocation_details)
docs.register(get_instance_details)

docs.register(filter_on_ancestor)
docs.register(get_data_item)
docs.register(get_data)
docs.register(was_derived_from)
docs.register(derived_data)
docs.register(get_data_granule_terms)
docs.register(derived_data)

docs.register(summaries_handler_workflow)
docs.register(summaries_handler_collab)

docs.register(export_data_provenance)
docs.register(export_run_provenance)




   

