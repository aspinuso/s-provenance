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
import logging
import sys
import os

from flask_apispec import use_kwargs, marshal_with, doc, FlaskApiSpec
from marshmallow import fields, Schema


app = Flask(__name__)
app.config['DEBUG'] = True
logging=os.environ['RAAS_LOGGING']

class PetSchema(Schema):
    class Meta:
        fields = ('name', 'category', 'size')


def bootstrap_app():
    app.db=provenance.ProvenanceStore(os.environ['RAAS_REPO'])
    return app

@app.route("/")
def hello():
    return "This is the s-prov service"



# the <method> can indicate value-range, hasAncherstorWith or the id of the resource
@app.route("/data/filterOnAncestor", methods=['GET','POST'])
def filter_on_ancestor():
        keylist = None
        vluelist= None
        mxvaluelist= None
        mnvaluelist= None
        idlist=None
        response = Response()

        if request.method == 'POST':
            try:
                memory_file = StringIO.StringIO(kwargs['ids']);
                idlist = csv.reader(memory_file).next()
                memory_file = StringIO.StringIO(kwargs['terms']);
                keylist = csv.reader(memory_file).next()
            #if (self.path=="values-range"):
                memory_file = StringIO.StringIO(kwargs['maxvalues']) if 'maxvalues' in kwargs else None
                mxvaluelist = csv.reader(memory_file).next()
                memory_file2 = StringIO.StringIO(kwargs['minvalues']) if 'minvalues' in kwargs else None
                mnvaluelist = csv.reader(memory_file2).next()
                memory_file2 = StringIO.StringIO(kwargs['values']) if 'values' in kwargs else None
                vluelist = csv.reader(memory_file2).next()
                dataid =StringIO.StringIO(kwargs['dataid']) if 'dataid' in kwargs else None
        
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
    

 
# Thomas
# Insert sequences of provenance documents, these can be bundles or lineage. The documents can be in JSON or JSON-LD. Format adaptation for storage purposes is handled by the acquisition function.

@app.route("/workflowexecutions/insert", methods=['POST'])
@use_kwargs({'prov': fields.Str()})
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
def wfexec_description_edit(runid,**kwargs):
        
        #if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":POST WorkflowRunInfo - "+runid);
        payload = kwargs["doc"]
        response = Response(json.dumps(app.db.editRun(runid,json.loads(str(payload)))))
        response.headers['Content-type'] = 'application/json'
        return response

#Deletes the bundle and all the lineage documents related to the \emph{run\_id}.

@app.route("/workflowexecutions/<runid>/delete", methods=['POST'])
def delete_workflow_run(runid):
         
        if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":POST workflowexecution delete - "+runid+" PID:"+str(os.getpid()));
        response = Response(json.dumps(app.db.deleteRun(runid)))
        response.headers['Content-type'] = 'application/json'
        return response


#Extract documents from the bundle collection by the \id{run\_id} of a \emph{WFExecution} 


paging ={ 'start': fields.Int(required=True),
          'limit': fields.Int(required=True)
          }

 

queryargsnp = {'usernames': fields.Str(),
             'terms': fields.Str(),
             'maxvalues': fields.Str(),
             'minvalues': fields.Str(),
             'wasAssociatedWith': fields.Str(),
             'implementations' : fields.Str(),
             'types': fields.Str(),
             'mode': fields.Str(),
             'format': fields.Str(),
             'rformat': fields.Str(missing="json")
              }

queryargs =dict(queryargsnp,**paging)

@app.route("/workflowexecutions/<runid>", methods=['GET', 'DELETE'])
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
@use_kwargs(queryargs)
def get_workflow_executions(**kwargs):
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
    implementations = csv.reader(StringIO.StringIO(kwargs['implementations'])).next() if 'implementations' in kwargs else None
    
    formats = csv.reader(StringIO.StringIO(kwargs['formats'])).next() if ('formats' in kwargs and kwargs['formats']!="") else None
    types = csv.reader(StringIO.StringIO(kwargs['types'])).next() if 'types' in kwargs else None
    mode = kwargs['mode'] if 'mode' in kwargs else 'OR'

    # type = csv.reader(StringIO.StringIO(kwargs['type'])) if 'type' in request.args else None

    if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET workflowexecutions -  PID:"+str(os.getpid()));
    response = Response()
    # chec functions above in root "/workflow/user/<user>""

    
    if keylist == None and implementations == None and formats==None and usernames!=None:
        response = Response(json.dumps(app.db.getWorkflowExecution(int(start),int(limit),usernames=usernames)))
    else: 
        response = Response(json.dumps(app.db.getWorkflowExecutionByLineage(int(start),int(limit),usernames=usernames, associatedWith=wasAssociatedWith, implementations=implementations, keylist=keylist,maxvalues=maxvalues,minvalues=minvalues, mode=mode, types=types,formats=formats)))

    response.headers['Content-type'] = 'application/json'    
    return response


#Extract information about the invocation or instances related to specified \emph{WFExecution} (\id{run\_id}), such as \emph{lastEventTime}, runtime \emph{messages}, indication on the generation of data, its accessibility and its total count. Such a result-set can be used for runtime monitoring, showing progress, data availability and anomalies. Details about a single invocation or  an instance can also be accessed by specifying its $id$. 
@app.route("/workflowexecutions/<runid>/instances")
@use_kwargs(paging)
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
@use_kwargs(levelargs)
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
def get_invocation_details(invocid):
        
        if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET invocation details - "+invocid+" PID:"+str(os.getpid()));
        response = Response()
        response = Response(json.dumps(app.db.getInvocation(invocid)))
        response.headers['Content-type'] = 'application/json'       
        return response


#Extract details about a single invocation or an instance by specifying their $id$.
instances=dict({"wasAssociateFor":fields.Str()},**paging)
@app.route("/instances/<instid>")
@use_kwargs(instances)
def get_instance_details(instid,**kwargs): 
        limit = int(kwargs['limit']) if 'limit' in kwargs else None
        start = int(kwargs['start']) if 'start' in kwargs else None
        runIds = csv.reader(StringIO.StringIO(kwargs['wasAssociateFor'])).next() if 'wasAssociateFor' in kwargs else None
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
def get_data_item(data_id): 
       
    response = Response(json.dumps(app.db.getData(0,1,id=str(data_id))))
    response.headers['Content-type'] = 'application/json'       
    return response

# Thomas
#The data is selected by specifying its id or a $query\_string$. Query parameters allow to search by \emph{attribution}, \emph{generation} and by combining more metadata terms with their \emph{value-ranges}. Attribution will match all entities of the S-PROV model such as \emph{ComponentInstances}, \emph{Components}, \emph{prov:Person},  while generation will consider \emph{Invocation} and \emph{WorkflowExecution}.
dataargs=dict({'wasGeneratedBy':fields.Str(),
               'wasAttributedTo':fields.Str()},**queryargs)

@app.route("/data")
@use_kwargs(dataargs)
def get_data(**kwargs):
        limit = kwargs['limit'] 
        start = kwargs['start']
        if logging == "True" : app.logger.info(str(datetime.datetime.now().time())+":GET data collection - PID:"+str(os.getpid()));
        #run
        genby = kwargs['wasGeneratedBy'] if 'wasGeneratedBy' in kwargs else None
        #component
        attrTo = kwargs['wasAttributedTo'] if 'wasAttributedTo' in kwargs else None
        #implementation
        implementations = kwargs['implementations'] if 'implementations' in kwargs else None
        keylist = csv.reader(StringIO.StringIO(kwargs['terms'])).next() if 'terms' in kwargs else None
        maxvalues = csv.reader(StringIO.StringIO(kwargs['maxvalues'])).next() if 'maxvalues' in kwargs else None
        minvalues = csv.reader(StringIO.StringIO(kwargs['minvalues'])).next() if 'minvalues' in kwargs else None
        format = kwargs['format'] if 'format' in kwargs else None
        mode = kwargs['mode'] if 'mode' in kwargs else 'OR'
        #id = kwargs['id'] if 'id' in kwargs else None
        
        response = Response(json.dumps(app.db.getData(int(start),int(limit),impl=implementations,genBy=genby,attrTo=attrTo,keylist=keylist,maxvalues=maxvalues,minvalues=minvalues,id=None,format=format,mode=mode)))

        response.headers['Content-type'] = 'application/json'

        return response

#Thomas
@app.route("/data/<data_id>/derivedData")
@use_kwargs(levelargsnp)
def derived_data(data_id,**kwargs):
    level = kwargs['level']
    if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+":GET derivedData - "+data_id+" PID:"+str(os.getpid()));
    response = Response(json.dumps(app.db.getDerivedDataTrace(data_id,int(level))))
    response.headers['Content-type'] = 'application/json'       
    return response

#Thomas
@app.route("/data/<data_id>/wasDerivedFrom")
@use_kwargs(levelargsnp)
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
@use_kwargs(termsargs)
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
                  'maxtme':fields.Str()
                  },**levelargsnp)

@app.route("/summaries/workflowexecution")
@use_kwargs(summaryargs)
def summaries_handler_workflow(**kwargs):
        if logging == "True" :  app.logger.info(str(datetime.datetime.now().time())+": GET getSummaries workflow - level= "+kwargs['level']);
        
        # the db function can be split in two to serve worklfow executions and collaborative views with explicit parameters
        response = Response(json.dumps(app.db.getActivitiesSummaries(**kwargs)))
        response.headers['Content-type'] = 'application/json'    
        return response

# Thomas check value-range level
# Extract information about the reuse and exchange of data between workflow executions, users and infrastructures, based terms and values' ranges. These Additional properties, such as workflow's type or (\id{prov:type})  can be also extracted

colargs=dict(dict({'groupby':fields.Str()},**queryargsnp),**levelargsnp)

@app.route("/summaries/collaborative")
@use_kwargs(colargs)
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



export=dict({'format':fields.Str()},**levelargsnp)
# EXPORT to PROV methods
@app.route("/data/<data_id>/export")
@doc(params={'level': {'description': 'The number of dependencies levels to extract'}})
@use_kwargs(export)
def export_data_provenance(data_id,**kwargs):
    response = Response(str(app.db.exportDataProvenance(data_id,**kwargs)).encode('ascii','ignore'))
    if 'format' in kwargs and kwargs['format']=='rdf':
        response.headers['Content-type'] = 'application/turtle' 

    else:
        response.headers['Content-type'] = 'application/xml' 
    return response


format=dict({'format':fields.Str()})
@app.route("/workflowexecutions/<run_id>/export")
@use_kwargs(format)
def export_run_provenance(run_id,**kwargs):
    response = Response(str(app.db.exportRunProvenance(run_id,**kwargs)).encode('ascii','ignore'))
    if 'format' in kwargs and kwargs['format']=='rdf':
        response.headers['Content-type'] = 'application/turtle' 
    else:
        response.headers['Content-type'] = 'application/xml' 
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
        description="S-ProvFlow provenance API - Provenance framework for storage and access of data-intensive streaming lineage. It offers a a web API and a range of dedicated visualisation tools and a provenance model (S-PROV) which utilises and extends PROV and ProvONE model"
    
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
    })
docs = FlaskApiSpec(app)


docs.register(insert_provenance)
docs.register(wfexec_description_edit)
docs.register(delete_workflow_run)

docs.register(get_workflow_info)
docs.register(get_instances_monitoring)
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




   

