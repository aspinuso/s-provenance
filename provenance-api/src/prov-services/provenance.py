from pymongo import *
import exceptions
import traceback
from prov.model import ProvDocument, Namespace, Literal, PROV, Identifier
import datetime
import dateutil.parser
import uuid
import traceback
import os
import socket   
import json
import httplib, urllib
import csv
import StringIO
from urlparse import urlparse
from itertools import chain
import sys
import helper as helper

sys.setrecursionlimit(10000)

def getUniqueId(data=None):
    if data is None:
        return socket.gethostname() + "-" + \
            str(os.getpid()) + "-" + str(uuid.uuid1())
    else:
        print("ID: "+str(id(data))+" DATA: "+str(data))
        return socket.gethostname() + "-" + \
            str(os.getpid()) + "-" + str(self.instanceId)+ "-" +str(id(data))

def makeHashableList(listobj,field):
     listobj=[x[field] for x in listobj]
     return listobj

def clean_empty(d):
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [v for v in (clean_empty(v) for v in d) if v]
    return {k: v for k, v in ((k, clean_empty(v)) for k, v in d.items()) if v}

  

def formatArtifactDic(dic):
 for x in dic:
     if type(dic[x])==list:
         dic[x]=str(dic[x])
 return dic
     

def resolveMissingTerms(trace):
    if "iterationId" not in trace:
            trace["iterationId"]=trace["instanceId"]
    if "worker" not in trace:
            trace["worker"]="NaN"
    if "actedOnBehalfOf" not in trace:
            trace["actedOnBehalfOf"]=trace["name"]
    return trace
     
     
def toW3Cprov(ling,bundl,format='xml',mode="run",bundle_type=None,bundle_creator="anonymous"):
        entities={}
        g = ProvDocument()
        vc = Namespace("s-prov", "http://s-prov/ns/#")  # namespaces do not need to be explicitly added to a document
        knmi = Namespace("knmi", "http://knmi.nl/ns/#")
        prov = Namespace("prov", "http://www.w3.org/ns/prov#")
        provone = Namespace("provone", "http://purl.dataone.org/provone/2015/01/15/ontology#")
        con = Namespace("con", "http://verce.eu/control")
        var = Namespace("var", "http://schema.org#")
        g.add_namespace("dcterms", "http://purl.org/dc/terms/")
        g.add_namespace("vcard", "http://www.w3.org/2006/vcard/ns")
        
        'specify bundle'
        
        bundleid=getUniqueId()
        bundle=g.bundle(var[bundleid])
        be=g.entity(var[bundleid], {'prov:type': vc[bundle_type]})
        'specifing user that asked for the bundle'
        bcreator=g.agent(knmi["ag_"+bundle_creator],other_attributes={"dcterms:creator":bundle_creator})  # first time the ex namespace was used, it is added to the document automatically
        g.wasAttributedTo(be,bcreator)

        
        for trace in bundl:
            'specifing user that executed the workflow'
            
            ag=g.agent(knmi[trace["username"]],other_attributes={"prov:type":"provone:User", "vcard:uuid":trace["username"]})  # first time the ex namespace was used, it is added to the document automatically
            
            if 'ns' in trace:
                for x in trace['ns']:
                    g.add_namespace(x,trace['ns'][x])

           

                
            if trace['type']=='workflow_run':
                
                trace.update({'runId':trace['_id']})
                #bundle.wasAttributedTo(knmi[trace["runId"]], knmi["ag_"+trace["creator"]])
               
                
                
                dic={}
                i=0
                
                for key in trace:
                    
                
                    if key != "input":
                        if ':' in key:
                            dic.update({key: trace[key]})
                        
                        if key == "modules" or key == "source":
                                continue
                        
                        elif key == "tags":
                            dic.update({vc[key]: str(trace[key])})
                        #else:
                        #    dic.update({knmi[key]: trace[key]})
                dic.update({'prov:type': vc['WFExecution']})
                WFE=bundle.activity(knmi[trace["runId"]], None, None, dic)
                WFE.wasAssociatedWith(knmi[trace["runId"]], ag)
                
                dic={}
                i=0

                

                if 'prov:type' in trace:

                    try:
                        cla=g._namespaces[str(trace['prov:type'].split(':')[0])]
                        provtype=cla[trace['prov:type'].split(':')[1]]
                        WFE._attributes[prov['type']].add(provtype)
                    except:
                        provtype=var[str(trace['prov:type'])]
                        WFE._attributes[prov['type']].add(provtype)

                
                 
                if 'input' in trace:
                    if type(trace['input'])!=list:
                        trace['input']=[trace['input']]

                    wp = bundle.collection(knmi["WFPar_"+trace["_id"]], other_attributes={'prov:type': vc['WFExecutionInputs']} )
                    for y in trace['input']:
                        dic.update({'prov:type': vc['Data']})
                        for key in y:
                            if ':' in key:
                                dic.update({key: y[key]})
                            else:
                                dic.update({vc[key]: y[key]})
                        

                        dt = bundle.collection(knmi[trace["_id"]+"_"+str(i)], formatArtifactDic(dic))
                        bundle.hadMember(wp,dt)
                        i=i+1
                        
                    bundle.used(knmi[trace["runId"]], wp)
                    
                    
        'specify lineage'
        for trace in ling:
            trace = resolveMissingTerms(trace)
            
           
            'specifing creator of the activity (to be collected from the registy)'
        
            #if 'creator' in trace:
            #    bundle.agent(knmi["ag_"+trace["creator"]],other_attributes={"dcterms:creator":trace["creator"]})  # first time the ex namespace was used, it is added to the document automatically
            #    bundle.wasAttributedTo(knmi[trace["runId"]], knmi["ag_"+trace["creator"]])
                
            'adding activity information for lineage'
            dic={}
            for key in trace:
                
                if type(trace[key])!=list:
                    if ':' in key:
                        dic.update({key: trace[key]})
                    else:
                        
                        if key=='location':
                            
                            dic.update({"prov:location": trace[key]})    
                        else:
                            dic.update({knmi[key]: trace[key]})
            
            
                
            if "Invocation_"+trace["iterationId"] not in entities:
                ac=bundle.activity(knmi["Invocation_"+trace["iterationId"]], trace["startTime"], trace["endTime"], other_attributes=dic.update({'prov:type': vc["Invocation"]}))
                entities["Invocation_"+trace["iterationId"]]=ac
                bundle.wasAssociatedWith(ac,knmi["ComponentInstance_"+trace["instanceId"]])
            else:
                ac=entities["Invocation_"+trace["iterationId"]]
                if (str(ac.get_endTime())<trace["endTime"]):
                   ac=entities["Invocation_"+trace["iterationId"]]
                   ac.set_time(ac.get_startTime(), trace["endTime"])
            
            
            if "ComponentInstance_"+trace["instanceId"] not in entities:
                #print(str(y[trace['prov_cluster'].split(':')[0]]))
                provtype=""

                #check whether qualified
               



                  
                        
                ag=bundle.agent(knmi["ComponentInstance_"+trace["instanceId"]], other_attributes={"prov:type":provtype,"prov:type":vc["ComponentInstance"],vc["worker"]:trace['worker'],vc["pid"]:trace['pid']})
                
                if 'prov_cluster' in trace:
                    try:
                        cla=g._namespaces[str(trace['prov_cluster'].split(':')[0])]
                        provtype=cla[trace['prov_cluster'].split(':')[1]]
                    except:
                        provtype=var[str(trace['prov_cluster'])]


                ag._attributes[prov['type']].add(provtype)

                entities["ComponentInstance_"+trace["instanceId"]]=1
                bundle.actedOnBehalfOf(knmi["ComponentInstance_"+trace["instanceId"]],knmi["Component_"+trace["actedOnBehalfOf"]+"_"+trace["runId"]])
                
            
            
            if "Component_"+trace["actedOnBehalfOf"]+"_"+trace["runId"] not in entities:
                ag=bundle.agent(knmi["Component_"+trace["actedOnBehalfOf"]+"_"+trace["runId"]], other_attributes={"prov:type":vc["Component"],"s-prov:functionName":trace["name"]})
                entities["Component_"+trace["actedOnBehalfOf"]+"_"+trace["runId"]]=1
                bundle.wasAssociatedWith(WFE,knmi["Component_"+trace["actedOnBehalfOf"]+"_"+trace["runId"]])
                bundle.wasAssociatedWith(knmi["Invocation_"+trace["iterationId"]],knmi["Component_"+trace["actedOnBehalfOf"]+"_"+trace["runId"]],)
                #bundle.hadPlan
              
               
            'adding parameters to the document as input entities'
            dic={}
            for x in trace["parameters"]:
                if ':' in x["key"]:
                    dic.update({x["key"]: x["val"]})
                else:
                    dic.update({knmi[x["key"]]: x["val"]})
                
            dic.update({'prov:type':vc['ComponentParameters']})
            
            
            bundle.entity(knmi["CPar_"+trace["instanceId"]], formatArtifactDic(dic))
            bundle.used(knmi['Invocation_'+trace["iterationId"]], knmi["CPar_"+trace["instanceId"]], identifier=knmi["used_"+trace["iterationId"]])

            'adding input dependencies to the document as input entities'
            dic={}
        
            for x in trace["derivationIds"]:
                'state could be added'   
            #dic.update({'prov:type':'parameters'})
            
                if 'DerivedFromDatasetID' in x and x['DerivedFromDatasetID']:
                
                    #if "Data_"+x["DerivedFromDatasetID"] not in entities:
                    #    c1=bundle.collection(knmi["Data_"+x["DerivedFromDatasetID"]])
                    #    entities["Data_"+x["DerivedFromDatasetID"]]=c1
                    #    print "USED"
                    #else:
                    #    print "EXisTS"
                    #    c1=entities["Data_"+x["DerivedFromDatasetID"]] 
                           
                    bundle.used(knmi['Invocation_'+trace["iterationId"]], knmi["Data_"+x["DerivedFromDatasetID"]], identifier=knmi["used_"+trace["iterationId"]+"_"+x["DerivedFromDatasetID"]])



            'adding entities to the document as output metadata'
            for x in trace["streams"]:
                i=0
                state=None
                parent_dic={}
                for key in x:
                        if key=='indexedMeta':
                            continue
                        if key=='con:immediateAccess':
                            
                            parent_dic.update({knmi['immediateAccess']: x[key]}) 
                        elif key=='location':
                            parent_dic.update({"prov:location": str(x[key])})
                        elif key=='port':
                            None
                        elif key == 'content':
                            None
                        else:
                            parent_dic.update({vc[key]: helper.num(x[key])})
                

                parent_dic.update({'prov:type':vc['Data']})           
                 
            
                
                #if "Data_"+x["id"] not in entities:
                if knmi["Data_"+x["id"]] not in entities:
                    c1=bundle.collection(knmi["Data_"+x["id"]],other_attributes=parent_dic)
                    entities[knmi["Data_"+x["id"]]]=1

                 
                    
                    bundle.wasGeneratedBy(knmi["Data_"+x["id"]], knmi["Invocation_"+trace["iterationId"]], identifier=knmi["wgb_"+x["id"]])
                
                    if 'port' in x and (x['port']=='state' or x['port']=='_d4p_state'):
                        state=bundle.collection(knmi["StateCollection_"+trace["instanceId"]])
                        bundle.hadMember(state,c1)

                    if state!=None:
                        bundle.wasAttributedTo(state,knmi["ComponentInstance_"+trace["instanceId"]])



                    dd=0
                    for d in trace['derivationIds']:
                        if 'DerivedFromDatasetID' in x and x['DerivedFromDatasetID']:
                            bundle.wasDerivedFrom(knmi["Data_"+x["id"]], knmi["Data_"+d['DerivedFromDatasetID']],identifier=knmi["wdf_"+x["id"]+"_"+d['DerivedFromDatasetID']])
                            dd+=1
                
                    for y in x["content"]:
                
                        dic={}
                
                        if isinstance(y, dict):
                            val=None
                            for key in y:
                        
                                val =helper.num(y[key])
                                
                                
                            
                                if ':' in key:

                                    dic.update({key: val})

                                else:
                                    dic.update({knmi[key]: val})
                        else:
                            dic={knmi['text']:y}
                    
                        dic.update({'prov:type':vc['DataGranule']})
                 
                     
                    
                        e1=bundle.entity(knmi["DataGranule_"+x["id"]+"_"+str(i)], dic)
                    
                    # add further semantics classes to the data    
                        
                        if 'prov:type' in y:
                             
                            try:
                                cla=g._namespaces[y['prov:type'].split(':')[0]]
                                e1._attributes[prov['type']].add(cla[y['prov:type'].split(':')[1]])
                            except:

                                e1._attributes[prov['type']].add(var['prov:type'])

                            #print(e1._attributes)
                         
                        bundle.hadMember(knmi["Data_"+x["id"]], e1)
                    
                    i=i+1

        if format =='w3c-prov-json':
            return str(g.serialize(format='json'))
        elif format=='png':
            output = StringIO.StringIO()
            g.plot('test.png')
            return output
        else:
            return g.serialize(format=format)

class ProvenanceStore(object):


    LINEAGE_COLLECTION='lineage'
    BUNDLE_COLLECTION='workflow'
    TERM_SUMMARIES_COLLECTION='term_summaries'

    def __init__(self, url):
 
        self.connection = MongoClient(url, 27017)
        self.db = self.connection[os.environ["SPROV_DB"]]
        self.lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
        self.workflow = self.db[ProvenanceStore.BUNDLE_COLLECTION]
        self.count=0
        
        'too specific here, have to be migrated to gateway-api'
        #self.solver = db['solver']
        
    'extract information about a list of workflow runs starting from start to limit'    
    
#suport for rest call on workflow resources 
    def getWorkflows(self,**kwargs):
        #db = self.connection["verce-prov"]
        try:
            keylist=None
            maxvaluelist=None
            minvaluelist=None
            if 'idlist' in kwargs:
                memory_file = StringIO.StringIO(kwargs['idlist'][0])
                idlist = csv.reader(memory_file).next()
                
                return self.getUserRunbyIds(kwargs['username'][0],idlist,**kwargs)
            else:
               try:
                    memory_file = StringIO.StringIO(kwargs['keys'][0]) if 'keys' in kwargs else None
                    keylist = csv.reader(memory_file).next() 
                    memory_file = StringIO.StringIO(kwargs['maxvalues'][0]); 
                    maxvaluelist = csv.reader(memory_file).next()
                    memory_file2 = StringIO.StringIO(kwargs['minvalues'][0]);
                    minvaluelist = csv.reader(memory_file2).next()
               except:
                    None;
                 #return {'success':False, 'error':'Invalid Query Parameters'}
               
               return self.getUserRunsValuesRange(kwargs['username'][0],keylist,maxvaluelist,minvaluelist,**kwargs)
  
        except Exception:
            traceback.print_exc()
            raise 
        #self.getUserRuns(kwargs['username'][0],**kwargs)
        
#suport for rest call on entities resources         
    def getEntities(self,**kwargs):
        keylist=None
        maxvaluelist=None
        minvaluelist=None
        vluelist=None
        try:
            memory_file = StringIO.StringIO(kwargs['keys'][0]) if 'keys' in kwargs else None
            keylist = csv.reader(memory_file).next()
            memory_file = StringIO.StringIO(kwargs['maxvalues'][0]);
            maxvaluelist = csv.reader(memory_file).next()
            memory_file = StringIO.StringIO(kwargs['minvalues'][0]);
            minvaluelist = csv.reader(memory_file).next()
            memory_file = StringIO.StringIO(request.args['values'][0]) if 'values' in kwargs else None
            vluelist = csv.reader(memory_file).next() if memory_file != None else None
            
            return self.getEntitiesBy(kwargs['method'][0],keylist,maxvaluelist,minvaluelist,vluelist,**kwargs)
  
        except Exception:
             
            traceback.print_exc()
            return self.getEntitiesBy(kwargs['method'][0],keylist,maxvaluelist,minvaluelist,vluelist,**kwargs)
            
        
    def makeElementsSearchDic(self,keylist,mnvaluelist,mxvaluelist):
        elementsDict={}
        
        for x in keylist:
            maxval=mxvaluelist.pop(0)
            minval=mnvaluelist.pop(0)
            maxval =helper.num(maxval)
            minval =helper.num(minval)
            
                
            elementsDict.update({x:{"$lte":maxval,"$gte":minval }})
        
        searchDic={'streams.content':{'$elemMatch':elementsDict}}
        return searchDic
    
    def getEntitiesFilter(self,searchDic,keylist,mxvaluelist,mnvaluelist,start,limit):
            elementsDict ={}
            searchContextDic={}
            # db = self.connection["verce-prov"]
            # # lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
            #if iterationId!=None:
            
            if keylist==None:
                print "Filter Query: "+str(searchDic)
                obj = self.lineage.find(searchDic,{"runId":1,"streams":1,"parameters":1,'startTime':1,'endTime':1,'errors':1,'derivationIds':1,'iterationId':1,'prov_cluster':1}).sort("endTime",direction=-1)[start:start+limit]
                totalCount = self.lineage.count(searchDic)
                #self.lineage.count(searchDic)
                return (obj,totalCount)
            else:
                
                for x in keylist:
                    
                    maxval=mxvaluelist.pop(0)
                    minval=mnvaluelist.pop(0)
                    maxval =helper.num(maxval)
                    minval =helper.num(minval)
                   

                
                    elementsDict.update({x:{"$lte":maxval,"$gte":minval }})
                    searchContextDic={'streams.content':{'$elemMatch':elementsDict}}
                    
                    searchDic.update(searchContextDic)
                    
                    
                 
                print "Filter Query: "+str(searchContextDic)
                #obj =  self.lineage.find(activ_searchDic,{"runId":1,"streams.content.$":1,'endTime':1,'errors':1,"parameters":1})[start:start+limit].sort("endTime",direction=-1)
                obj= self.lineage.aggregate(pipeline=[{'$match':searchContextDic},
                                                    {"$unwind": "$streams" },
                                                    #{ "$unwind": "$streams.content" },
                                                    
                                                    {'$group':{'_id':'$_id', 'derivationIds':{ '$first': '$derivationIds' },'parameters': { '$first': '$parameters' },'runId': { '$first': '$runId' },'endTime': { '$first': '$endTime' },'startTime': { '$first': '$startTime' },'errors': { '$first': '$errors' },'streams':{ '$push':{'content' :'$streams.content','format':'$streams.format','location':'$streams.location','id':'$streams.id'}}}},
                                                    
                                                    ]) 

                totalCount=self.lineage.find(activ_searchDic,{"runId":1}).count()
                return (obj,totalCount)
                    
            
            
            
            
    
    
    
    
    def exportDataProvenance(self, id, **kwargs):
        
        
        # db = self.connection["verce-prov"]
        # workflow = self.db[ProvenanceStore.BUNDLE_COLLECTION]
        # # lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
        totalCount=self.lineage.find({'runId':id}).count()
        
        tracelist=[]
        if 'level' in kwargs:  
            self.getTraceList(id, helper.num(kwargs['level']),tracelist) 
            
              #self.lineage.find({'runId':id}).sort("endTime",direction=-1)
            
        bundle=self.workflow.find({"_id":tracelist[0]['runId']}).sort("startTime",direction=-1)
        
        if 'format' in kwargs:
            return toW3Cprov(tracelist,bundle,format = kwargs['format'],bundle_type="WFDataTraceBundle")
        else:
            return toW3Cprov(tracelist,bundle,bundle_type="WFDataTraceBundle")
            
            
    
    
    def exportRunProvenance(self, id,**kwargs):
        
        
        # db = self.connection["verce-prov"]
        # workflow = self.db[ProvenanceStore.BUNDLE_COLLECTION]
        # # lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
        #totalCount=self.lineage.find({'runId':id}).count()
        cursorsList=list()
        
       
        bundle=self.workflow.find_one({"_id":id})
        username=bundle['username']
        lineage=self.lineage.find({'runId':id,'username':username})
        #.sort("endTime",direction=-1)
         
       # bundle=self.workflow.find({"_id":id}).sort("startTime",direction=-1)
        
        if 'format' in kwargs:

            return toW3Cprov(lineage,[bundle],format = kwargs['format'],bundle_type="WFExecutioinBundle")
        else:
            
            return toW3Cprov(lineage,[bundle],bundle_type="WFExecutioinBundle")
            
       
    
    def exportAllRunProvenance(self, id,**kwargs):
        
        
        
        # db = self.connection["verce-prov"]
        # # lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
        totalCount=self.lineage.find({'runId':id}).count()+1
        cursorsList=list()
        
        if ('start' in kwargs and int(kwargs['start'][0])==0):
            cursorsList.append(self.workflow.find({"_id":id}))
        
        
        if 'all' in kwargs and kwargs['all'][0].upper()=='TRUE':
            
            cursorsList.append(self.lineage.find({'runId':id})[int(kwargs['start'][0]):int(kwargs['start'][0])+int(kwargs['limit'][0])].sort("endTime",direction=-1))
             
        else:
            cursorsList.append(self.lineage.find({'runId':id})[int(kwargs['start'][0]):int(kwargs['start'][0])+int(kwargs['limit'][0])].sort("endTime",direction=-1))

        exportDocList = list()
        
        
        
        
        
        for cursor in cursorsList:    
            for x in cursor:
                if 'format' not in kwargs or kwargs['format'][0].find('w3c-prov')!=-1:
                    
                    exportDocList.app(x,format = kwargs['format'][0] if 'format' in kwargs else 'w3c-prov-json')
        
        output = exportDocList
        
      
        return  (output,totalCount)
    
    def getSolverConf(self,id,userId=None):
        db = self.connection["verce-prov"]
        solver = db['solver']
        try:
            solver = solver.find_one({"_id":id})
            if (solver!=None):
                solver.update({"success":True})
                if userId!=None:
                    def userFilter(item): 
                        return (not "users" in item) or (userId and userId in item["users"])
                    def velmodFilter(item):
                        item["velmod"] = filter(userFilter, item["velmod"])
                        return item
                    solver["meshes"] = map(velmodFilter, filter(userFilter, solver["meshes"]))
                return solver
            else:
                return {"success":False, "error":"Solver "+path+" not Found"}
            
        except Exception, e:
            return {"success":False, "error":str(e)}
    
    
    
    def getUserRunbyIds(self,userid,id_list,**kwargs):
        
         
        runids=[]
        # db = self.connection["verce-prov"]
        # workflow = self.db[ProvenanceStore.BUNDLE_COLLECTION]
        obj=self.workflow.find({"_id":{"$in":id_list},'username':userid},{"startTime":-1,"system_id":1,"description":1,"name":1,"workflowName":1,"grid":1,"resourceType":1,"resource":1,"queue":1}).sort("startTime",direction=-1)
        totalCount=self.workflow.find({"_id":{"$in":id_list}}).sort("startTime",direction=-1).count()
        for x in obj:
            
            runids.append(x)
        
            
        output = {"runIds":runids};
        output.update({"totalCount": totalCount})
        
        return output
    
    
    def getUserRunsValuesRange(self,userid,keylist,maxvaluelist,minvaluelist,**kwargs):
        # db = self.connection["verce-prov"]
        # workflow = self.db[ProvenanceStore.BUNDLE_COLLECTION]
        # # lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
        elementsDict ={}
        output=None
        runids=[]
        uniques=None
        totalCount=0
        start=int(kwargs['start'][0])
        limit=int(kwargs['limit'][0])
        if keylist==None: 
            keylist=[]
        
        if ((keylist==None or len(keylist)==0) and 'activities' not in kwargs):
            return self.getUserRuns(userid, **kwargs)
        
        if 'activities' in kwargs:
             
            values=str(kwargs['activities'][0]).split(',')
            intersect=False
            
            for y in values:
                 
                #curs=self.lineage.find({'username':userid,'name':y})
                 
                uniques_act=self.lineage.aggregate(pipeline=[{'$match':{'username':userid,'name':y}},
                                                    {'$group':{'_id':'$runId','startTime':{ '$first': '$startTime' }}},
                                                    {'$sort':{'startTime':-1}},
                                                    {'$project':{'_id':1}}]) 
                
                 
                uniques_act=makeHashableList(uniques_act,'_id')
                
                if intersect==True:
                    uniques=list(set(uniques).intersection(set(uniques_act)))
                else:
                    uniques=uniques_act
                    intersect=True
                
         
         
        if len(keylist)!=0 and "mime-type" in keylist:
            values=list((set(minvaluelist).union(set(maxvaluelist))))
            #totalCount=totalCount+len(self.lineage.find({'username':userid,'streams.format':{'$in':values}}).distinct("runId"))
            uniques_mime=self.lineage.aggregate(pipeline=[{'$match':{'username':userid,'streams.format':{'$in':values}}},
                                                    {'$group':{'_id':'$runId','startTime':{ '$first': '$startTime' }}},
                                                    {'$sort':{'startTime':-1}},
                                                    {'$project':{'_id':1}}
                                                    ]) 
            
            #self.lineage.find({'username':userid,'streams.format':{'$in':values}}).distinct("runId")
            uniques_mime=makeHashableList(uniques_mime,'_id')

            i = keylist.index('mime-type')
            minvaluelist.pop(i)
            maxvaluelist.pop(i)
            keylist.remove('mime-type')
            
            if uniques!=None:
                uniques=list(set(uniques).intersection(set(uniques_mime)))
            else:
                uniques=uniques_mime
        
        
        for x in keylist:
            maxval=maxvaluelist.pop(0)
            minval=minvaluelist.pop(0)
            maxval =helper.num(maxval)
            minval =helper.num(minval)
            
            objdata=self.lineage.aggregate(pipeline=[{'$match':{'username':userid,'streams.content':{'$elemMatch':{x:{"$lte":maxval,"$gte":minval }}}}},
                                                    {'$group':{'_id':'$runId','startTime':{ '$first': '$startTime' }}},
                                                    {'$sort':{'startTime':-1}},
                                                    {'$project':{'_id':1}}
                                                    ]) 
            objdata=makeHashableList(objdata,'_id')
            #self.lineage.find({'username':userid,'streams.content':{'$elemMatch':{x:{"$lte":maxval,"$gte":minval }}}},{"startTime":-1,'runId':1}).sort("startTime",direction=-1).distinct("runId") 
            objpar=self.lineage.aggregate(pipeline=[{'$match':{'username':userid,'parameters':{'$elemMatch':{'key':x,'val':{"$lte":maxval,"$gte":minval }}}}},
                                                    {'$group':{'_id':'$runId','startTime':{ '$first': '$startTime' }}},
                                                    {'$sort':{'startTime':-1}},
                                                    {'$project':{'_id':1}}
                                                    ]) 
            objpar=makeHashableList(objpar,'_id')
            #self.lineage.find({'username':userid,'parameters':{'$elemMatch':{'key':x,'val':{"$lte":maxval,"$gte":minval }}}},{"startTime":-1,'runId':1}).sort("startTime",direction=-1).distinct("runId")           
              
            object_union=list(set(objdata).union(set(objpar)))
            
             
            
            if uniques!=None:
                 
                uniques=list(set(uniques).intersection(set(object_union)))
                 
            else:
                uniques=object_union
                
      
       
        totalCount=len(uniques)
        
        #uniques=[x['_id'] for x in uniques]
        
        obj=self.workflow.find({"_id":{"$in":uniques[start:start+limit]}},{"startTime":-1,"system_id":1,"description":1,"name":1,"workflowName":1,"grid":1,"resourceType":1,"resource":1,"queue":1}).sort("startTime",direction=-1)
         
        for x in obj:
            
            runids.append(x)
        
            
        output = {"runIds":runids};
        output.update({"totalCount": totalCount})
        return output
    
    
    def getEntitiesByValuesRange(self,path,keylist,mtype,start,limit,runId=None,iterationId=None,dataId=None,maxvaluelist=None,minvaluelist=None,valuelist=None):
         
        elementsDict ={}
        output=None
        runids=[]
        uniques=None
       
        for x in keylist:
            maxval=maxvaluelist.pop(0)
            minval=minvaluelist.pop(0)
            maxval =helper.num(maxval)
            minval =helper.num(minval)
             
            if runId!=None:
                
                objdata=self.lineage.find({'runId':runId,'streams.format':mtype,'streams.content':{'$elemMatch':{x:{"$lte":maxval,"$gte":minval }}}},{"runId":1,"streams.content.$":1,'streams':1,'startTime':1,'endTime':1,'errors':1,"parameters":1}) 
                objpar=self.lineage.find({'runId':runId,'streams.format':mtype,'parameters':{'$elemMatch':{'key':x,'val':{"$lte":maxval,"$gte":minval }}}},{"runId":1,"streams.content.$":1,'streams':1,'startTime':1,'endTime':1,'errors':1,"parameters":1}) 
                
                object_union=list(set(objdata).union(set(objpar)))
                
                
            else:
                
                objdata=self.lineage.find({'streams.format':mtype,'streams.content':{'$elemMatch':{x:{"$lte":maxval,"$gte":minval }}}},{"runId":1,"streams.content.$":1,'streams':1,'startTime':1,'endTime':1,'errors':1,"parameters":1}) 
                objpar=self.lineage.find({'streams.format':mtype,'parameters':{'$elemMatch':{'key':x,'val':{"$lte":maxval,"$gte":minval }}}},{"runId":1,"streams.content.$":1,'streams':1,'startTime':1,'endTime':1,'errors':1,"parameters":1})            
                object_union=list(set(objdata).union(set(objpar)))
                
            if (uniques!=None):
                uniques=list(set(uniques).intersection(set(object_union)))
                
            else:
           
                uniques=object_union
                
        
        totalCount=len(uniques)
          
        
               
        
        
                    
        artifacts = list()

        
        for x in  uniques:
            
            for s in x["streams"]:
                totalCount=totalCount+1
                s["wasGeneratedBy"]=x["_id"]
                s["parameters"]=x["parameters"]
                s["endTime"]=x["endTime"]
                s["startTime"]=x["startTime"]
                s["runId"]=x["runId"]
                s["errors"]=x["errors"]
                artifacts.append(s)
                    
        
                
        output = {"entities":artifacts};
        output.update({"totalCount": totalCount})
        return  output
        
        
    
    def getRunInfo(self, path):
         # db = self.connection["verce-prov"]
         # workflow = self.db[ProvenanceStore.BUNDLE_COLLECTION]
         obj = self.workflow.find_one({"_id":path})
         return obj

         
     
    def getUserRuns(self, path, **kwargs):
        # db = self.connection["verce-prov"]
        workflow = self.db[ProvenanceStore.BUNDLE_COLLECTION]
        obj=None
        totalCount=None
        output=None
        start=int(kwargs['start'][0])
        limit=int(kwargs['limit'][0])
        
        
        if 'activities' in kwargs:
            return self.getUserRunsValuesRange(kwargs['username'][0],None,None,None,**kwargs)
        else:
            obj = self.workflow.find({"username":path},{"_id":-1,"startTime":-1,"system_id":1,"description":1,"name":1,"workflowName":1,"grid":1,"resourceType":1,"resource":1,"queue":1}).sort("startTime",direction=-1)[start:start+limit]

        totalCount=self.workflow.find({"username":path}).count()
        runids = list()
        
        for x in obj:
                
            runids.append(x)
            
        output = {"runIds":runids};
        output.update({"totalCount": totalCount})
    
        return  output
    
    
    def num(self,s):
        try:
            return int(s)
        except exceptions.ValueError:
            try:
                return float(s)
            except exceptions.ValueError:
                return s

     
    
    
    def getEntitiesBy(self,meth,keylist,mxvaluelist,mnvaluelist,vluelist,**kwargs):
        # db = self.connection["verce-prov"]
        # lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
        totalCount=0;
        cursorsList=list()
        obj=None
        
        start=int(kwargs['start'][0]) if 'start' in kwargs and kwargs['start'][0]!='null' else None
        limit=int(kwargs['limit'][0]) if 'limit' in kwargs and kwargs['limit'][0]!='null' else None
        runId=kwargs['runId'][0].strip() if 'runId' in kwargs and kwargs['runId'][0]!='null' else None
        dataId=kwargs['dataId'][0].strip() if 'dataId' in kwargs and kwargs['dataId'][0]!='null' else None
        iterationId=kwargs['iterationId'][0].strip() if 'iterationId' in kwargs and kwargs['iterationId'][0]!='null' else None
        mtype=kwargs['mime-type'][0].strip() if 'mime-type' in kwargs and kwargs['mime-type'][0]!='null' else None
        activities=None
        
        if 'activities' in kwargs:
            activities=str(kwargs['activities'][0]).split(',')
            
        i=0
        ' extract data by annotations either from the whole archive or for a specific runId'
         
        activ_searchDic={'_id':iterationId,'name':{'$in':activities},'runId':runId,'streams.format':mtype}
        
        activ_searchDic=clean_empty(activ_searchDic)
        
    
        
        
        if meth=="annotations":
            if runId!=None:
                for x in keylist:
                    cursorsList.append(self.lineage.find({'streams.annotations':{'$elemMatch':{'key': x,'val':{'$in':vluelist}}},'runId':runId},{"runId":1,"streams.annotations.$":1,'streams':1,'startTime':1,'endTime':1,'errors':1,"parameters":1,})[start:start+limit].sort("endTime",direction=-1))
                    totalCount = totalCount + self.lineage.find({'streams.annotations':{'$elemMatch':{'key': x,'val':{'$in':vluelist}}},'runId':runId},).count()
            else:
                for x in keylist:
                    cursorsList.append(self.lineage.find({'streams.annotations':{'$elemMatch':{'key': x,'val':{'$in':vluelist}}}},{"runId":1,"streams.annotations.$":1,'streams':1,'startTime':1,'endTime':1,'errors':1,"parameters":1})[start:start+limit].sort("endTime",direction=-1))
                    totalCount = totalCount + self.lineage.find({'streams.annotations':{'$elemMatch':{'key': x,'val':{'$in':vluelist}}}},).count()
        
        if meth=="generatedby":
            cursorsList.append(self.getEntitiesFilter(activ_searchDic,keylist,mxvaluelist,mnvaluelist,start,limit))
        elif meth=="run":        
            cursorsList.append(self.lineage.find({'runId':runId,'streams.id':dataId},{"runId":1,"streams":{"$elemMatch": { "id": dataId}},"parameters":1,'startTime':1,'endTime':1,'errors':1,'derivationIds':1}))
            totalCount = totalCount + self.lineage.find({'runId':runId,'streams.id':dataId}).count()
        elif meth=="values-range":

            cursorsList.append(self.getEntitiesFilter(activ_searchDic,keylist,mxvaluelist,mnvaluelist,start,limit))
        
        else:
            cursorsList.append(self.lineage.find({'streams.id':meth}))
                
            
        artifacts = list()

        for cursor in cursorsList:
            for x in cursor:
                
                for s in x["streams"]:
                     
                    if (mtype==None or mtype=="") or ('format' in s and s["format"]==mtype):
                        totalCount=totalCount+1
                        s["wasGeneratedBy"]=x["_id"]
                        s["parameters"]=x["parameters"]
                        s["endTime"]=x["endTime"]
                        s["startTime"]=x["startTime"]
                        s["runId"]=x["runId"]
                        s["errors"]=x["errors"]
                        s["derivationIds"]=x['derivationIds']
                        artifacts.append(s)
                    
        
                
        output = {"entities":artifacts};
        output.update({"totalCount": totalCount})
       
        return  output
         
    

    
    def editRun(self, id,doc):
        
        
        ret=[]
        response={}
        # db = self.connection["verce-prov"]
        workflow = self.db[ProvenanceStore.BUNDLE_COLLECTION]
        # lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
        try:
            
            self.workflow.update({"_id":id},{'$set':doc})
        
            response={"success":True}
            response.update({"edit":id}) 
        
        except Exception, err:
            response={"success":False}
            response.update({"error":str(err)})
            
        finally:
            return response
        
        
    def deleteRun(self, id):
        ret=[]
        response={}
        # db = self.connection["verce-prov"]
        # workflow = self.db[ProvenanceStore.BUNDLE_COLLECTION]
        # lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
        try:
            if (self.workflow.find_one({"_id":id})!=None):
                self.lineage.remove({"runId":id})
                self.workflow.remove({"_id":id})
            
                response={"success":True}
                response.update({"delete":id}) 
            else:
                response={"success":False}
                response.update({"error":"Workflow run "+id+" does not exist!"}) 
            
        except Exception, err:
            response={"success":False}
            response.update({"error":str(err)})
            traceback.print_exc()
        finally:
            return response
    
    def insertWorkflow(self, json):
        # db = self.connection["verce-prov"]
        #workflow = self.db[ProvenanceStore.BUNDLE_COLLECTION]
        ret=[]
        response={}
        
        try:
            if type(json) =='list':
        
                for x in json:
                    
                    ret.append(self.workflow.insert(x))
            else:
                ret.append(self.workflow.insert(json))
        
            response={"success":True}
            response.update({"inserts":ret}) 
        
        except Exception, err:
            response={"success":False}
            response.update({"error":str(err)}) 
        finally:
            return response
    
    
    ' insert new data in different collections depending from the document type'

    def updateCollections(self, prov):
        # db = self.connection["verce-prov"]
        ## lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
        #workflow = self.db[ProvenanceStore.BUNDLE_COLLECTION]
        try:
            if prov["type"]=="lineage":
                if prov["type"]=="lineage":
                #    return self.lineage.find_one_and_replace({'_id':prov['_id']},prov,upsert=True)
                # if(self.workflow.find_one({"_id":prov["runId"]})!=None):
                     return self.lineage.insert(helper.addIndexedContentToLineage(prov))
                # else: 
                #     raise Exception("Workflow Run not found")

            if prov["type"]=="workflow_run":    
                return self.workflow.update_one({'runId':prov['runId']},{"$set":prov},upsert=True).raw_result
        
        except Exception, err:
            raise err
            traceback.print_exc()
             
            
    def insertData(self, prov):
        # db = self.connection["verce-prov"]
        # workflow = self.db[ProvenanceStore.BUNDLE_COLLECTION]
        ret=[]
        response={}
        
        
        try:
            if type(prov).__name__ =='list':
                 
                for x in prov:
                   try:
                       ret.append(self.updateCollections(x))
                   except Exception, err:
                       ret.append({"error":str(err)})
            else:
                try:
                 
                    ret.append(self.updateCollections(prov))
                except Exception, err:
                       ret.append({"error":str(err)})
        
            response={"success":True}
            response.update({"inserts":ret}) 
        
        except Exception, err:
            
            response={"success":False}
            response.update({"error":str(err)}) 

            
        finally:

            return response
    
    
    def getDerivedDataTrace(self, id,level):
        # db = self.connection["verce-prov"]
        # lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
        xx = self.lineage.find_one({"streams.id":id},{"runId":1,"derivationIds":1,'streams.port':1,'streams.location':1});
        xx.update({"dataId":id})
        cursor=self.lineage.find({"derivationIds":{'$elemMatch':{"DerivedFromDatasetID":id}}},{"runId":1,"streams":1});
         
        
        if level>0:
            derivedData=[]
            
            i=0
            for d in cursor:
                i+=1
                if (i<25):
                 
                 
                 
                    for str in d["streams"]:
                     
                        try:
                            derivedData.append(self.getDerivedDataTrace(str["id"],level-1))
                        
                        except Exception, err:
                            None
                 
                 
                
            xx.update({"derivedData":derivedData})
        
        return xx
 



    # Wide first
    def getTrace(self, id,level):
            # db = self.connection["verce-prov"]
            # lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
            if type(id)!=list:
                id=[id]
            #if type(id)==list:
            self.count+=1
            curs = self.lineage.find({"streams.id":{"$in":id}},{'streams.content':1,
                                                                'streams.id':1,
                                                                'streams.port':1,
                                                                'streams.size':1,
                                                                'iterationId':1,
                                                                'iterationIndex':1,
                                                                'runId':1,
                                                                'streams.location':1,
                                                                'actedOnBehalfOf':1,
                                                                'derivationIds':1,
                                                                '_id':0
                                                                })
          
            nodes=[]

            for xx in curs:
                
                if "streams" not in xx:
                    continue

                derivations=[]
                if xx!=None and level>0:
                    #print(xx["derivationIds"])
                    listids=[]
                    props={}

                    for s in xx["streams"]:
                        if s["id"] not in id:
                            del s
                          
                    for derid in xx["derivationIds"]:
                        listids.append(derid["DerivedFromDatasetID"]) 
                        props[derid["DerivedFromDatasetID"]]={}
                        #set relelevant properties
                        if "up:assertionType" in derid:
                            props[derid["DerivedFromDatasetID"]]["up:assertionType"] = derid["up:assertionType"]
                        if "port" in derid and derid["port"]=='_d4p_state':
                            props[derid["DerivedFromDatasetID"]]["@type"] = "s-prov:StateDerivation"
                        if "port" in derid and derid["port"]!='_d4p_state':
                            props[derid["DerivedFromDatasetID"]]["@type"] = "s-prov:FlowDerivation"

                    try:
                        #xx["s-prov:Data"] = {"@id":derid["DerivedFromDatasetID"]}
                        derivations = self.getTrace(listids,level-1)
                        for x in derivations:
                            x.update(props[x["s-prov:Data"]['@id']])

                    except Exception, err:
                        traceback.print_exc()
                
                xx["s-prov:Data"]=xx['streams'][0]
                xx["s-prov:Data"]['@id']=xx["s-prov:Data"]['id']
                xx["s-prov:Data"]['prov:location']=xx["s-prov:Data"]['location']
                xx["s-prov:Data"]['prov:hadMember']=xx["s-prov:Data"]['content']
                
                for g in xx["s-prov:Data"]['prov:hadMember']:
                    g["@type"]="s-prov:DataGranule"

                xx["s-prov:Data"]['prov:hadMember']
                xx["s-prov:Data"]['prov:Derivation']=derivations
                xx["s-prov:Data"]["prov:wasGeneratedBy"]={}
                if 'iterationIndex' in xx:
                    xx["s-prov:Data"]["prov:wasGeneratedBy"]['s-prov:Invocation']={'@id':xx['iterationIndex']}
                    del xx['iterationIndex']
                if 'iterationId' in xx:
                    xx["s-prov:Data"]["prov:wasGeneratedBy"]['s-prov:Invocation']={'@id':xx['iterationId']}
                    del xx['iterationId']
                xx["s-prov:Data"]["prov:wasGeneratedBy"]['s-prov:WFExecution']={'@id':xx['runId']}
                xx["s-prov:Data"]["prov:wasAttributedTo"]={'@id':xx['actedOnBehalfOf'],'@type':'s-prov:Component'}
                del xx["s-prov:Data"]['location']
                del xx["s-prov:Data"]['content']
                del xx["s-prov:Data"]['id']
                del xx['runId']
                del xx["actedOnBehalfOf"]
                del xx["derivationIds"]
                del xx['streams']
                nodes.append(xx)
            return nodes



    
    # Deep first
    def getTraceDP(self, id,level):
         
        self.count+=1
        xx = self.lineage.find_one({"streams.id":id},{'streams':{'$elemMatch':{'id':id}},
                                                            'iterationId':1,
                                                            'runId':1,
                                                            'streams.location':1,
                                                            'actedOnBehalfOf':1,
                                                            'derivationIds':1,
                                                            '_id':0}
                                                            );
        if xx and "derivationIds" in xx and level>=0:
            #print(xx["derivationIds"])
            for derid in xx["derivationIds"]: 
    
                try:
                    derid["s-prov:Data"] = {"@id":derid["DerivedFromDatasetID"]}
    
                    derid["wasDerivedFrom"] = self.getTrace(derid["DerivedFromDatasetID"],level-1)
                 
                    if (derid["wasDerivedFrom"]):
                        derid["s-prov:Data"] = derid["wasDerivedFrom"]["s-prov:Data"]
                        del derid["wasDerivedFrom"]
                        del derid["DerivedFromDatasetID"]
                        del derid["TriggeredByProcessIterationID"]
                    else:
                        derid.clear()
                except Exception, err:
                    traceback.print_exc()
            
            xx["s-prov:Data"]=xx['streams'][0]
            xx["s-prov:Data"]['@id']=xx["s-prov:Data"]['id']
            xx["s-prov:Data"]['prov:location']=xx["s-prov:Data"]['location']
            xx["s-prov:Data"]['prov:hadMember']=xx["s-prov:Data"]['content']
            xx["s-prov:Data"]['prov:Derivation']=xx["derivationIds"]
            xx["s-prov:Data"]["prov:wasGeneratedBy"]={}
            xx["s-prov:Data"]["prov:wasGeneratedBy"]['s-prov:Invocation']={'@id':xx['iterationId']}
            xx["s-prov:Data"]["prov:wasGeneratedBy"]['s-prov:WFExecution']={'@id':xx['runId']}
            xx["s-prov:Data"]["prov:wasAttributedTo"]={'@id':xx['actedOnBehalfOf'],'@type':'s-prov:Component'}
            del xx["s-prov:Data"]['location']
            del xx["s-prov:Data"]['content']
            del xx["s-prov:Data"]['id']
            del xx['iterationId']
            del xx['runId']
            del xx["actedOnBehalfOf"]
            del xx["derivationIds"]
            del xx['streams']
            return xx

        
    def getTraceList(self, id,level,ll):
        sys.setrecursionlimit(2000)
        # db = self.connection["verce-prov"]
        ## lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
        xx = self.lineage.find_one({"streams.id":id});
        if xx!=None:
            xx.update({"id":id})
            ll.append(xx)
            if level>=0:
                for derid in xx["derivationIds"]:
                    if 'DerivedFromDatasetID' in derid and derid["DerivedFromDatasetID"]!=None and derid["DerivedFromDatasetID"]!=xx["id"]:
                        try:
                    
                            self.getTraceList(derid["DerivedFromDatasetID"],level-1,ll)
                    
                        except Exception, err:
                            traceback.print_exc()
                 
                return xx
        
        
        
  
        
    
    
    def filterOnAncestorsValuesRange(self,idlist,keylist,minvaluelist,maxvaluelist,level=100,mode='OR'):
        filteredIds=[]
        for x in idlist:

            test=self.hasAncestorWith_new(x,level,keylist,minvaluelist,maxvaluelist,mode=mode)
             
            if test!=None and test==True:
                filteredIds.append(x)
        
        return filteredIds
    
     
    
   
    
                
    def hasAncestorWithValuesRange(self, id, keylist,minvaluelist,maxvaluelist):
        # db = self.connection["verce-prov"]
        # lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
        elementsDict ={}
        k=0
        for x in keylist:
            maxval=maxvaluelist[k]
            minval=minvaluelist[k]
            k+=1
            maxval =helper.num(maxval)
            minval =helper.num(minval)
                
            if minval==maxval:
                elementsDict.update({x:maxval})
            else:
                elementsDict.update({x:{"$lte":maxval,"$gte":minval }})
        #print elementsDict
        xx = self.lineage.find_one({"streams.id":id},{"runId":1,"derivationIds":1});
        if xx!= None and len(xx["derivationIds"])>0:    
            for derid in xx["derivationIds"]:
                try:
                
                    anchestor = self.lineage.find_one({"streams":{"$elemMatch":{"id":derid["DerivedFromDatasetID"],'content':{'$elemMatch':elementsDict}}}},{"streams.id":1});
                    
                    if anchestor!=None:
                        return {"hasAncestorWith":True}
                    else:
                        return self.hasAncestorWithValuesRange(derid["DerivedFromDatasetID"],keylist,minvaluelist,maxvaluelist)
                except Exception,e: 
                   traceback.print_exc()
        else:
            return {"hasAncestorWith":False}
        
    
    def hasAncestorWith(self, id, keylist,valuelist):
         
        elementsDict ={}
        
        k=0
        for x in keylist:
            val=valuelist[k]
            k+=1
            val =helper.num(val)
            
            elementsDict.update({x:val})
        
        xx = self.lineage.find_one({"streams.id":id},{"runId":1,"derivationIds":1});
        if len(xx["derivationIds"])>0:    
            for derid in xx["derivationIds"]:
                try:
                
                    anchestor = self.lineage.find_one({"streams":{"$elemMatch":{"id":derid["DerivedFromDatasetID"],'content':{'$elemMatch':elementsDict}}}},{"streams.id":1});
                    
                    if anchestor!=None:
                        return {"hasAncestorWith":True}
                    else:
                        return self.hasAncestorWith(derid["DerivedFromDatasetID"],keylist,valuelist) 
                        #self.hasAncestorWith(derid["DerivedFromDatasetID"],keylist,valuelist)
                except Exception,e: 
                   traceback.print_exc()
        else:
            return {"hasAncestorWith":False}
       
        
        
    def getTraceConditonalX(self, id, keylist,valuelist):
        # db = self.connection["verce-prov"]
        # lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
        elementsDict ={}
        
        k=0
        for x in keylist:
            val=valuelist[k]
            k+=1
            val =helper.num(val)
            
            elementsDict.update({x:val})
        
        xx = self.lineage.find_one({"streams.id":id,'streams.content':{'$elemMatch':elementsDict}},{"runId":1,"derivationIds":1});
        
        if xx==None:
            xx = self.lineage.find_one({"streams.id":id},{"runId":1,"derivationIds":1});
             
            xx.update({"id":id})
            
            for derid in xx["derivationIds"]:
                try:
                    val = self.getTraceConditonal(derid["DerivedFromDatasetID"],keylist,valuelist)
                     
                    if val!=None:
                        return {"hasAnchestor":True}
                    
                except Exception, err:
                    traceback.print_exc()
            
        else:
            return xx
        
        
    def getActivitiesSummaries(self,**kwargs): 
        # db = self.connection["verce-prov"]
        # lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
        # workflow = self.db[ProvenanceStore.BUNDLE_COLLECTION]
        obj=[]
        runId=[]
        groupby=None
        clusters=None
        tags=None
        run=None
        users=None
        #print(kwargs)

        if 'runId' in kwargs:
             runId = kwargs['runId']
        if 'groupby' in kwargs:
            groupby=kwargs['groupby']
        if 'clusters' in kwargs:
            memory_file = StringIO.StringIO(kwargs['clusters']);
            clusters = csv.reader(memory_file).next()
       
        matchdic=clean_empty({'username':{'$in':users},'runId':runId, 'prov_cluster':{'$in':clusters} })
        
       
        start=dateutil.parser.parse(kwargs['mintime']) if 'mintime' in kwargs and kwargs['mintime']!='null' else None
        maxtime=dateutil.parser.parse(kwargs['maxtime']) if 'maxtime' in kwargs and kwargs['maxtime']!='null' else None
        matchdic=clean_empty(matchdic)
        
        if 'level' in kwargs and kwargs['level']=='prospective':
            if start!=None:
                matchdic.update({'startTime':{'$gt':str(start)}})
            obj=self.lineage.aggregate(pipeline=[{'$match':matchdic},{'$unwind': "$streams"},{'$group':{'_id':{'actedOnBehalfOf':'$actedOnBehalfOf','mapping':'$mapping',str(groupby):'$'+str(groupby)}, 'time':{'$min': '$startTime'}}},{'$sort':{'time':1}}]) 
            
        elif 'level' in kwargs and kwargs['level']=='iterations':
            matchdic.update({'startTime':{'$lt':str(maxtime)},'iterationIndex':{'$gte':int(kwargs['minidx']) ,'$lt':int(kwargs['maxidx'])}})
            if start!=None:
                matchdic.update({'startTime':{'$lt':str(maxtime)}})
            matchdic=clean_empty(matchdic)
            matchdic.update({'iterationId':{'$ne':None}})
            #print(matchdic)
            obj=self.lineage.aggregate(pipeline=[{'$match':matchdic},{'$unwind': "$streams"},{'$group':{'_id':{'iterationId':'$iterationId','mapping':'$mapping',str(groupby):'$'+str(groupby)}, 'time':{'$min': '$startTime'}}},{'$sort':{'time':1}}])
        elif 'level' in kwargs and kwargs['level']=='instances':
            if maxtime!=None:
                matchdic.update({'startTime':{'$lt':str(maxtime)}})
            print(matchdic)
            obj=self.lineage.aggregate(pipeline=[{'$match':matchdic},{'$unwind': "$streams"},{'$group':{'_id':{'instanceId':'$instanceId','mapping':'$mapping',str(groupby):'$'+str(groupby)}, 'time':{'$min': '$startTime'}}},{'$sort':{'time':1}}])
            
        elif 'level' in kwargs and (kwargs['level']=='vrange' or kwargs['level']=='data'):

            memory_file = StringIO.StringIO(kwargs['keys']);
            keylist = csv.reader(memory_file).next()
            memory_file = StringIO.StringIO(kwargs['maxvalues']);
            mxvaluelist = csv.reader(memory_file).next()
            memory_file = StringIO.StringIO(kwargs['minvalues']);
            mnvaluelist = csv.reader(memory_file).next()
            memory_file = StringIO.StringIO(kwargs['users']);
            users = csv.reader(memory_file).next()
            #memory_file = StringIO.StringIO(kwargs['tags']);
            #tags = csv.reader(memory_file).next()
            
            searchDic = self.makeElementsSearchDic(keylist,mnvaluelist,mxvaluelist)
             
            #print(" searchdic "+json.dumps(searchDic['streams.content']['$elemMatch']))
            if kwargs['level']=='vrange':
                if kwargs['mode']=="AND":
                    obj=self.lineage.aggregate(pipeline=[{'$match':{'username':{'$in':users},'streams.content':searchDic['streams.content']}},{'$group':{'_id': {'runId':'$runId','username':'$username', str(groupby):'$'+str(groupby)}}}])
                elif kwargs['mode']=="OR":
                    for y in searchDic['streams.content']['$elemMatch']:
                        for c in self.lineage.aggregate(pipeline=[{'$match':{'username':{'$in':users},'streams.content':{'$elemMatch':{y:searchDic['streams.content']['$elemMatch'][y]}}}},
                                                             {'$group':{'_id': {'runId':'$runId','username':'$username', str(groupby):'$'+str(groupby)}}}]):
                            obj.append(c)
                
        else:
            obj=self.lineage.aggregate(pipeline=[{'$match':{'runId':{'$in':runId}}},{'$group':{'_id':{'name':'$name'}}},{'$project':{'_id':1}}]) 
       
        
        connections=[]
        
        
        for x in obj:
             
            #add=True
            if not bool(x):
               del x
            
            if runId:
                 
                #run=x['_id']['run']
                x['_id'].update({'runId':runId})
                 
                #del x['_id']['run']
            
            trigger_cursor=None
            tringgers=[]
            if 'level' in kwargs and kwargs['level']=='vrange':
                try:
                    
                    trigger_cursor=self.workflow.aggregate(pipeline=[{'$match':{'_id':x['_id']['runId']}},{'$unwind':'$input'},{'$match':{'$or':[{'input.prov:type':'wfrun'},{'input.prov-type':'wfrun'}]}},{'$project':{'input.url':1,'_id':0}}])
                    #print 'TRIG '+str(x['_id'])+' '+ json.dumps(triggers)
                except:
                    traceback.print_exc()
                    triggers=[]
                
                    #print "wf ID "+str(x['_id'])
                try:

                    wfitem=self.workflow.find({'_id':x['_id']['runId']},{groupby:1,'_id':0})
                    if groupby in wfitem:
                        x['_id'].update(wfitem) 
                    else:
                        continue
                        #print "wfname"+str(wfitem['workflowName'])
                except:
                    traceback.print_exc()
                    #print "wf ID "+str(x['_id']['runId'])+" not found inf workflow collection"
                    del x
                    continue
                     
                     
            elif 'level' in kwargs and (kwargs['level']=='instances' or kwargs['level']=='iterations' or kwargs['level']=='prospective'):
                if maxtime!=None:
                    x['_id'].update({'startTime':{'$lt':str(maxtime)}})
                trigger_cursor=self.lineage.aggregate(pipeline=[{'$match':x['_id']},{'$unwind':'$derivationIds'},{'$group':{'_id':'$derivationIds.DerivedFromDatasetID'}}])  
            elif 'level' in kwargs and kwargs['level']=='data':
                trigger_cursor=self.lineage.aggregate(pipeline=[{'$match':{'streams.id':x['_id']['id']}},{'$unwind':'$derivationIds'},{'$project':{'_id':0,'id':'$derivationIds.DerivedFromDatasetID'}}]) 

            triggers=[]
            
            for t in trigger_cursor:
                #print(t)
                if '_id' in t and t['_id']!=None:
                    
                    
                    triggers.append(t['_id'])
                else:
                    triggers.append(t)
               
                
                
            
            
            
            if len(triggers)>0:
                #print "triggers "+str(x['_id'])+" "+str(triggers)
                pes=[]
                #print "DOING CONN"
                 
                if 'level' in kwargs and kwargs['level']=='prospective':
                    pes=self.lineage.aggregate(pipeline=[{'$match':{'streams.id':{'$in':triggers}}},{'$unwind':'$streams'},{'$group':{'_id':{'actedOnBehalfOf':'$actedOnBehalfOf'},'size':{'$sum':'$streams.size'}}}])
                elif 'level' in kwargs and kwargs['level']=='iterations':
                    pes=self.lineage.aggregate(pipeline=[{'$match':{'iterationId':{'$ne':None}, 'streams.id':{'$in':triggers}}},{'$unwind':'$streams'},{'$group':{'_id':{'iterationId':'$iterationId'},'size':{'$sum':'$streams.size'}}}])
                elif 'level' in kwargs and kwargs['level']=='instances':
                    pes=self.lineage.aggregate(pipeline=[{'$match':{'streams.id':{'$in':triggers}}},{'$unwind':'$streams'},{'$group':{'_id':{'instanceId':'$instanceId'},'size':{'$sum':'$streams.size'}}}]) 
                elif 'level' in kwargs and kwargs['level']=='vrange':
                    for w in triggers:
                        up=urlparse(w['input']['url']).path
                        up=up[up.rfind('/')+1:len(up)+1]
                         
                        curs=self.workflow.find({'_id':up})
                        if (curs.count()>0):
                            pes.append(up)
                elif 'level' in kwargs and kwargs['level'][0]=='data':
                    pes=triggers
                else:
                    pes=self.lineage.aggregate(pipeline=[{'$match':{'$or':triggers}},{'$project':{'name':1,"_id":0}}]) 
                
                #x['_id']['runId']=run
                pelist=[]
                
                for pe in pes:
                    
                    pelist.append(pe)
                    
                    
                x.update({'name':x['_id'], 'connlist':pelist})
                
                #print "connections done for: "+str(x['_id'])+" PES:"+str(pelist)
                #print "size for: "+str(x['_id'])+" PES:"+str(pelist)
                
                
                del x['_id']
                connections.append(x)
                
                 
#             
            else: 
                 
                x.update({'name':x['_id'], 'connlist':[]})
                del x['_id']
                connections.append(x)
                
        return connections
    
    
    ' methods for the updated API'



    def getCollaborativeSummariesWorkfows(self,mode="OR",groupby="username",keylist=None,maxvalues=None,minvalues=None,users=None):
        # lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
        # workflow = self.db[ProvenanceStore.BUNDLE_COLLECTION]
        obj=[]

        key_value_pairs = helper.getKeyValuePairs(keylist, maxvalues, minvalues)

        
        if mode=="AND":
            aggregate_pipeline = [
                {
                    '$match':{
                        'username':{
                            '$in':users
                        },
                        '$or': helper.getIndexedMetaQueryList(key_value_pairs) + helper.getParametersQueryList(key_value_pairs)
                    }
                },
                {
                    '$unwind': '$streams'
                },
                {   
                    '$unwind': '$streams.indexedMeta'
                },
                {
                    '$group':{
                        '_id': {
                            'runId':'$runId',
                            'username':'$username', 
                            str(groupby):'$'+str(groupby)
                        },
                        'indexedMeta': { 
                            '$addToSet': "$streams.indexedMeta"
                        }
                    }
                },
                {
                    '$match': {
                        '$and': helper.getAndQueryList(key_value_pairs)
                    }
                }
            ]
            #print(aggregate_pipeline)
            aggregate_results = self.lineage.aggregate(pipeline=aggregate_pipeline)
            for aggregate_result in aggregate_results:    
                obj.append(aggregate_result)

        elif mode=="OR":
            aggregate_pipeline = [
                {
                    '$match':{
                        'username':{
                            '$in':users
                        },
                        '$or': helper.getIndexedMetaQueryList(key_value_pairs) + helper.getParametersQueryList(key_value_pairs)
                    }
                },
                {
                    '$group':{
                        '_id': {
                            'runId':'$runId',
                            'username':'$username', 
                            str(groupby):'$'+str(groupby)
                        }
                    }
                }
            ]
            aggregate_results = self.lineage.aggregate(pipeline=aggregate_pipeline)
            for aggregate_result in aggregate_results:    
                obj.append(aggregate_result)


        runIds=[]


        for x in obj:
            runIds.append(x['_id']['runId'])
        
        connections=[]
        #print(runIds)
        for x in obj:
            
            trigger_cursor=None
            tringgers=[]

            #looks for dependencies
            try:
                trigger_cursor=self.workflow.aggregate(pipeline=[{'$match':{'_id':x['_id']['runId']}},{'$unwind':'$input'},{'$match':{'$or':[{'input.prov:type':'wfrun'},{'input.prov-type':'wfrun'}]}},{'$project':{'input.url':1,'_id':0,groupby:1}}])
#                 trigger_cursor=self.workflow.find({'_id':x['_id']['runId'],'$or':[{'input.prov:type':'wfrun'},{'input.prov-type':'wfrun'}]},{'input.url':1,'_id':0})
                
                 
            except:
                traceback.print_exc()
                triggers=[]
                
            
            #extracts run grouping property
            #print "wf ID "+str(x['_id'])
            try:

                wfitem=self.workflow.find_one({'_id':x['_id']['runId']},{groupby:1,'_id':0})
                if wfitem is not None and groupby in wfitem:
                    x['_id'].update(wfitem) 
                else:
                    continue
            except:
                traceback.print_exc()
                #print "wf ID "+str(x['_id']['runId'])+" not found inf workflow collection"
                del x
                continue


            triggers=[]
            #x['_id'].update(trigger_cursor.next()[groupby])
            for t in trigger_cursor:
                #print(t)

                if '_id' in t and t['_id']!=None:
                    
                    
                    triggers.append(t['_id'])
                else:
                    triggers.append(t)

            if len(triggers)>0:
                #print("triggers "+str(x['_id'])+" "+str(len(triggers)))
                pes=[]
                #print "DOING CONN"
                 
                for w in triggers:
                    up=urlparse(w['input']['url']).path
                    up=up[up.rfind('/')+1:len(up)+1]
                    if (up in runIds):
                        pes.append(up)
                
                pelist=[]
                for pe in pes:
                    
                    pelist.append(pe)
                    
                    
                x.update({'name':x['_id'], 'connlist':pelist})
                
                #print "connections done for: "+str(x['_id'])+" PES:"+str(pelist)
                #print "size for: "+str(x['_id'])+" PES:"+str(len(pes))
                
                
                del x['_id']
                connections.append(x)
            else: 
                x.update({'name':x['_id'], 'connlist':[]})
                del x['_id']
                connections.append(x)
        return connections
             
    
    def getEntitiesGeneratedBy(self,runid,invocationid,start,limit):
        cursorsList=[]
        activ_searchDic={'iterationId':invocationid,'runId':runid}
        cursorsList.append(self.getEntitiesFilter(activ_searchDic,None,None,None,start,limit))
        entities=[]
        
        totalCount=0
        for cursor in cursorsList:
            for x in cursor:
                 
                for s in x["streams"]:
                     
                    totalCount=totalCount+1
                    s["wasGeneratedBy"]=x["iterationId"]
                    s["parameters"]=x["parameters"]
                    s["endTime"]=x["endTime"]
                    s["startTime"]=x["startTime"]
                    s["runId"]=x["runId"]
                    s["errors"]=x["errors"]
                    s["derivationIds"]=x['derivationIds']
                    entities.append(s)
                    
        
                
        output = {"entities":entities};
        output.update({"totalCount": totalCount})
       
        return  output


    def getEntitiesAttributedToInstnace(self,runid,instanceId,start,limit):
        cursorsList=[]
        activ_searchDic={'instanceId':instanceId,'runId':runid}
        cursorsList.append(self.getEntitiesFilter(activ_searchDic,None,None,None,start,limit))
        entities=[]
        
        totalCount=0
        for cursor in cursorsList:
            for x in cursor:
                 
                for s in x["streams"]:
                     
                    totalCount=totalCount+1
                    s["wasGeneratedBy"]=x["iterationId"]
                    s["parameters"]=x["parameters"]
                    s["endTime"]=x["endTime"]
                    s["startTime"]=x["startTime"]
                    s["runId"]=x["runId"]
                    s["errors"]=x["errors"]
                    s["derivationIds"]=x['derivationIds']
                    entities.append(s)
                    
        
                
        output = {"entities":entities};
        output.update({"totalCount": totalCount})
       
        return  output


    # new methods for new API returning JSON-LD


    def addLDContext(self,obj):
        obj["@context"]={"s-prov" : "https://raw.githubusercontent.com/KNMI/s-provenance/master/resources/s-prov-o.owl#",
                            "prov" : "http://www.w3.org/ns/prov-o#",
                            "oa" : "http://www.w3.org/ns/oa.rdf#",
                            "vcard" : "http://www.w3.org/2006/vcard/ns#",
                            "provone" : "http://purl.org/provone"}
        return obj

    def getMonitoring(self, id,level,start,limit):
        # db = self.connection["verce-prov"]
        # lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
        group=''
        if level=="invocation":
               group='iterationId'
        elif level=="instance":
               group='instanceId'
        elif level=="component":
               group='actedOnBehalfOf'
        elif level=="cluster":
               group='prov_cluster'

        else:   
               group='instanceId'

        obj = self.lineage.aggregate(pipeline=[{'$match':{'runId':id}},
                                                    
                                                    {"$unwind":"$streams"},
                                                    {'$group':{'_id':'$'+group, 
                                                     "s-prov:lastEventTime":{"$max":"$endTime"}, 
                                                     "s-prov:message":{"$push":"$errors"},
                                                     "s-prov:worker":{"$first":"$worker"},
                                                     "prov:actedOnBehalfOf":{"$first":"$actedOnBehalfOf"}, 
                                                     "s-prov:generatedWithImmediateAccess":{"$push":"$streams.con:immediateAccess"},
                                                     "s-prov:generatedWithLocation":{"$push":"$streams.location"},
                                                     "s-prov:qualifiedChange": {"$push":"$s-prov:qualifiedChange"},
                                                     "s-prov:dataCount":{"$push":"$streams.id"}}},
                                                     {"$sort":{"s-prov:lastEventTime":-1}},
                                                     {'$skip':start},
                                                     {'$limit':limit},
                                                     ])

        count = self.lineage.aggregate(pipeline=[{'$match':{'runId':id}},
                                                    {'$group':{'_id':'$'+group}},
         
                                                    {"$count":group}])

        totalCount=0
        for x in count:
            totalCount=x[group]
#{'$project':{"runId":1,"instanceId":1,"parameters":1,"endTime":-1,"errors":1,"iterationIndex":1,"iterationId":1,"streams.con:immediateAccess":1,"streams.location":1}
       # self.lineage.find({'runId':id},{"runId":1,"instanceId":1,"parameters":1,"endTime":-1,"errors":1,"iterationIndex":1,"iterationId":1,"streams.con:immediateAccess":1,"streams.location":1})[start:start+limit].sort("endTime",direction=-1)
         
        activities = list()
        
        for x in obj:
           x['@id']=x['_id']
           del x['_id']
           if level=="invocation":
               x['@type']='s-prov:Invocation'
           elif level=="instance":
               x['@type']='s-prov:ComponentInstance'
           elif level=="component":
               x['@type']='s-prov:Component'
           elif level=="cluster":
               x['@type']=x['@id']

           activities.append(x)

           x['s-prov:message']=''.join(x['s-prov:message'])
           
           if type(x['s-prov:generatedWithLocation'])==list:
                flat_list=[]
                for sublist in x['s-prov:generatedWithLocation']:
                    for item in sublist:
                        flat_list.append(item)
                x['s-prov:generatedWithLocation']=flat_list

           x['s-prov:generatedWithLocation']=''.join(x['s-prov:generatedWithLocation'])
           x['s-prov:generatedWithLocation']=True if x['s-prov:generatedWithLocation']!="" else False
           x['s-prov:generatedWithImmediateAccess']= True if ("true" in x['s-prov:generatedWithImmediateAccess'] or True in x['s-prov:generatedWithImmediateAccess']) else False
           #x['s-prov:hasChanged']=True if len(x['feedbackInvocation'])!=0 else False
           x['s-prov:dataCount'] = len(x['s-prov:dataCount'])
           
           if level=="component" or level=="cluster":
               del x['prov:actedOnBehalfOf']
           else:
               x['prov:actedOnBehalfOf'] = {"@type":"s-prov:Component", "@id":x['prov:actedOnBehalfOf']}
           
           
            
        output = {"@graph":activities};
  
        output=self.addLDContext(output)
        output["totalCount"]= totalCount
        return  output


    def getComponentInstance(self, id, runIds=None,start=None,limit=None):
        # db = self.connection["verce-prov"]
        # lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
        searchdic={}
        if runIds==None:
            searchdic = {'instanceId':id} 
            start=0
            limit=1
        else:
            searchdic = {'instanceId':id,"runId":{"$in":runIds}}

        
        obj = self.lineage.aggregate(pipeline=[{'$match':searchdic},
                                                    {"$unwind":"$streams"},
                                                    {"$sort":{"endTime":-1}},
                                                    {'$group':{'_id':{"s-prov:ComponentInstance":'$instanceId', "s-prov:WFExecution":"$runId"},
                                                     "s-prov:lastEventTime":{"$max":"$endTime"}, 
                                                     "s-prov:message":{"$push":"$errors"},
                                                     "worker":{"$first":"$worker"}, 
                                                     "s-prov:generatedWithImmediateAccess":{"$push":"$streams.con:immediateAccess"},
                                                     "s-prov:generatedWithLocation":{"$push":"$streams.location"},
                                                     "s-prov:dataCount":{"$push":"$streams.id"},
                                                     "pid" : {"$first":"$pid"},
                                                     "mapping" : {"$first":"$mapping"},
                                                     "s-prov:qualifiedChange": {"$push":"$s-prov:qualifiedChange"},
                                                     "s-prov:ComponentParameters": {"$first":"$parameters"},
                                                     "prov:contributed":{"$first":"$name"}, 
                                                     "prov:actedOnBehalfOf":{"$first":"$actedOnBehalfOf"}, 
                                                     "prov_cluster":{"$first":"$prov_cluster"}}},
                                                     {"$skip": start},
                                                     {"$limit": limit}
                                                     #{ "$project": { "@id":"$_id", "_id":0, "s-prov:worker":1, "s-prov:lastEventTime":1, "s-prov:message":1,"s-prov:generatedWithImmediateAccess":1,"s-prov:generatedWithLocation":1,"s-prov:count":1}}
                                                    ])
      
        
        output={}
        count = self.lineage.aggregate(pipeline=[{'$match':{'instanceId':id}},
                                                    {'$group':{'_id':'$instanceId'}},
                                                    {"$count":'instanceNum'}])

        for x in count:
            totalCount=x['instanceNum']


        for x in obj:
            
            x['@id']=x['_id']["s-prov:ComponentInstance"]
            x['@type']='s-prov:ComponentInstance'
            x['prov:type']='s-prov:ComponentInstance'
            x['prov:atLocation']= {"@type" : "s-prov:SystemProcess",
                "s-prov:pid" : x["pid"],
                "s-prov:mapping" : x["mapping"],
                "s-prov:worker" : x["worker"]}

            x['prov:actedOnBehalfOf'] = {"@type":"s-prov:Component", "@id":x['prov:actedOnBehalfOf']}
            x['prov:contributed'] = {"@type":"s-prov:Implementation", "@id":x['prov:contributed']}
            x['prov:wasAssociateFor'] = {"@id":x["_id"]["s-prov:WFExecution"], "@type":"s-prov:WFExecution"}
            
            x['s-prov:message']=''.join(x['s-prov:message'])
           
            if type(x['s-prov:generatedWithLocation'])==list:
                flat_list=[]
                for sublist in x['s-prov:generatedWithLocation']:
                    for item in sublist:
                        flat_list.append(item)
                x['s-prov:generatedWithLocation']=flat_list

            x['s-prov:generatedWithLocation']=''.join(x['s-prov:generatedWithLocation'])
            x['s-prov:generatedWithLocation']=True if x['s-prov:generatedWithLocation']!="" else False
            x['s-prov:generatedWithImmediateAccess']= True if ("true" in x['s-prov:generatedWithImmediateAccess'] or True in x['s-prov:generatedWithImmediateAccess']) else False
            #x['s-prov:count'] = len(x['s-prov:count'])


             
            
            del x['_id']
            del x["pid"]
            del x["mapping"]
            del x["worker"]
            del x['prov_cluster']
            
            output=x

        output=self.addLDContext(output)
        output["totalCount"]= totalCount
        return output


    def getInvocation(self, id): 
        # db = self.connection["verce-prov"]
        # lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
        obj = self.lineage.aggregate(pipeline=[{'$match':{'iterationId':id}},
                                                    {'$group':{'_id':'$iterationId', 
                                                     "s-prov:lastEventTime":{"$max":"$endTime"}, 
                                                     "s-prov:message":{"$push":"$errors"},
                                                     #"worker":{"$first":"$worker"}, 
                                                     #"s-prov:generatedWithImmediateAccess":{"$push":"$streams.con:immediateAccess"},
                                                     #"s-prov:generatedWithLocation":{"$push":"$streams.location"},
                                                     "s-prov:dataCount":{"$push":"$streams.id"},
                                                     #"pid" : {"$first":"$pid"},
                                                     #"mapping" : {"$first":"$mapping"},
                                                     "s-prov:qualifiedChange": {"$push":"$s-prov:qualifiedChange"},
                                                     "s-prov:ComponentParameters": {"$first":"$parameters"},
                                                     #"prov:contributed":{"$first":"$name"}, 
                                                     "s-prov:ComponentInstance":{"$first":"$instanceId"}, 
                                                     #"prov:actedOnBehalfOf":{"$first":"$actedOnBehalfOf"}, 
                                                     "prov_cluster":{"$first":"$prov_cluster"}}}
                                                     #{ "$project": { "@id":"$_id", "_id":0, "s-prov:worker":1, "s-prov:lastEventTime":1, "s-prov:message":1,"s-prov:generatedWithImmediateAccess":1,"s-prov:generatedWithLocation":1,"s-prov:count":1}}
                                                    ]) 
        
        output={}
        count = self.lineage.aggregate(pipeline=[{'$match':{'iterationId':id}},
                                                    {'$group':{'_id':'$iterationId'}},
                                                    {"$count":'invocNum'}])

        for x in count:
            totalCount=x['invocNum']


        for x in obj:
            
            x['@id']=x['_id']
            x['@type']='s-prov:Invocation'
            x['prov:type']='s-prov:Invocation'
            x['prov:wasAssociatedWith']= {"@type" : "s-prov:ComponentInstance",
                
                "@id" : x["s-prov:ComponentInstance"]}

            
            x['s-prov:message']=''.join(x['s-prov:message'])
           
            del x['_id']
            #del x["pid"]
            #del x["mapping"]
            del x["s-prov:ComponentInstance"]
            #del x["worker"]
            del x['prov_cluster']
            
            output=x

        output=self.addLDContext(output)
        output["totalCount"]= totalCount
        return output


    def getComponent(self, id,runIds=None,start=None,limit=None):
        # db = self.connection["verce-prov"]
        # workflow = self.db[ProvenanceStore.BUNDLE_COLLECTION]
        # lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]

        obj = self.workflow.find({"source": {"$exists":{id:True}}, "_id":{"$in":runIds}},{'runId':1, 'source':1})

#{ "$unwind": "$provone:hasSubProcess" },
#                                           {"$group":{"_id":"$provone:hasSubProcess.prov:wasAttributedTo.@id",
#                                            "@type":{"$first":"$provone:hasSubProcess.prov:wasAttributedTo.@type"},
#                                            "s-prov:CName":{"$first":"$provone:hasSubProcess.prov:wasAttributedTo.s-prov:CName"},
#                                            "prov:hadPlan":{"$first":"$provone:hasSubProcess"},
#                                            "runId":{"$first":"$runId"}
#                                            }},
#                                           {'$match': {"_id": {"$eq": id}}
        ln = self.lineage.aggregate(pipeline=[{'$match':{'actedOnBehalfOf':id, "runIds": {"$in":runIds}}},
                                                    {'$group':{'_id':'$actedOnBehalfOf', 
                                                     "s-prov:qualifiedChange": {"$push":"$s-prov:qualifiedChange"},
                                                     "s-prov:ComponentParameters": {"$first":"$parameters"},
                                                     "prov_cluster":{"$first":"$prov_cluster"}}}
                                                      
                                                     #{ "$project": { "@id":"$_id", "_id":0, "s-prov:worker":1, "s-prov:lastEventTime":1, "s-prov:message":1,"s-prov:generatedWithImmediateAccess":1,"s-prov:generatedWithLocation":1,"s-prov:count":1}}
                                                    ]) 
        
       
       
        x=obj.next()
        
        x["prov:wasAssociateFor"]={"@type":"s-prov:WFExecution","@id":x["runId"]}
        
        for inst in ln:
            if "s-prov:qualifiedChange" in inst and (len(inst["s-prov:qualifiedChange"])>0):
                x["s-prov:qualifiedChange"]=inst["s-prov:qualifiedChange"]
                for change in x["s-prov:qualifiedChange"]:
                    change.update({"s-prov:ComponentInstance":{"@id":inst["_id"]}})

        x["@id"]=id
        x["s-prov:CName"]=id
        x["@type"]="s-prov:Component"
        x["prov:wasAssociateFor"]["prov:hadPlan"]={}
        x["prov:wasAssociateFor"]["prov:hadPlan"]["s-prov:source"]=x["source"][id]["code"]
        x["prov:wasAssociateFor"]["prov:hadPlan"]
        x["prov:wasAssociateFor"]["prov:hadPlan"]["@type"]="s-prov:Implementation"
        x["prov:wasAssociateFor"]["prov:hadPlan"]["s-prov:functionName"]=x["source"][id]["functionName"]
        x["s-prov:type"]=x["source"][id]["type"]
        del x["_id"]
        del x["runId"]
        del x["source"]

        
        self.addLDContext(x)
        return x

    def getData(self,start,limit,impl=None,genBy=None,attrTo=None,keylist=None,maxvalues=None,minvalues=None,id=None,format=None,mode='OR',clusters=None):
        print('start getData--> start: ', start, ' limit: ', limit, ' genBy: ', genBy, 'format:',format,' attrTo: ', attrTo, ' keylist: ', keylist, ' maxvalues: ', maxvalues, ' minvalues: ', minvalues, ' id: ', id)
        # db = self.connection["verce-prov"]
        # lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
        streamItems=[]
        totalCount=1
        if id != None:
            print('---- is not none')
            (streamItems, totalCount)=self.getEntitiesFilter_new({'streams.id':id},keylist,maxvalues,minvalues,start,limit, mode,format)



        else:
            totalCount=0;
            searchAgents=None
            searchImplementations=None
            searchActivities=None
            cursorsList=[]
            
            activities=None
            
            if attrTo!=None:
                entities=attrTo.split(',')
                searchAgents=[{'actedOnBehalfOf':{'$in':entities}},{'instanceId':{'$in':entities}},{'username':{'$in':entities}},{'name':{'$in':entities}}]
                

            if genBy!=None:
                activities=genBy.split(',')
                searchActivities=[{'iterationId':{'$in':activities}},{'runId':{'$in':activities}}]

            if impl!=None:
                activities=impl.split(',')
                searchImplementations=[{'name':{'$in':activities}}]

            if clusters!=None:
                pclusters=clusters.split(',')
                searchImplementations=[{'prov_cluster':{'$in':pclusters}}]
            
            # TODO format


            i=0
            ' extract data by annotations either from the whole archive or for a specific runId'
             
            searchDic={"$and":[{"$or":searchAgents},{"$or":searchActivities},{"$or":searchImplementations}]}
            searchDic=clean_empty(searchDic)
             
            print("--- SEARCH! -- "+str(searchDic)) 
            if searchDic!=None:
                (streamItems, totalCount)=self.getEntitiesFilter_new(searchDic,keylist,maxvalues,minvalues,start,limit, mode,format)
            
        output = {"@graph":streamItems};
        output=self.addLDContext(output)
        output.update({"totalCount": totalCount})
        print('---- is not none')
        return  output
        

    def getWorkflowExecutionByLineage(self, start, limit, usernames, associatedWith, implementations, keylist, maxvalues, minvalues, mode = 'OR', types=None,formats = None,clusters=None):
        print('usernames: ', usernames, 'implementations:', implementations,'keylist: ', keylist, 'maxvalues: ', maxvalues, 'minvalues: ', minvalues, 'mode: ', mode, 'format: ', formats, 'cluster: ', clusters)
        # lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
        # workflow = self.db[ProvenanceStore.BUNDLE_COLLECTION]
        aggregateResults=None
        
        # START: Build match
        aggregate_match = {}
        if usernames is not None and len(usernames) > 0: 
            aggregate_match['username'] = {
                '$in': usernames
            }

        if associatedWith is not None and len(associatedWith) > 0: 
            aggregate_match['actedOnBehalfOf'] = {
                '$in': associatedWith
            }
            aggregate_match['username'] = {
                '$in': associatedWith
            }

        

        if implementations is not None and len(implementations) > 0:

            aggregate_match['name'] = {
                    '$in': implementations
                    }

        if clusters is not None and len(clusters) > 0:

            aggregate_match['prov_cluster'] = {
                    '$in': clusters
                    }
        
        
        if formats is not None and keylist == None:
            aggregate_match['streams'] = {
                '$elemMatch': {
                    'format': {
                        '$in': formats
                    }
                }
            }



        #print(aggregate_match)
        key_value_pairs =[]
        if keylist is not None :
            key_value_pairs = helper.getKeyValuePairs(keylist, maxvalues, minvalues);
            print(key_value_pairs)
            indexed_meta_query = helper.getIndexedMetaQueryList(key_value_pairs)
            parameters_query = helper.getParametersQueryList(key_value_pairs)
            aggregate_match['$or'] = indexed_meta_query + parameters_query

            if formats is not None:
                aggregate_match['$or'] += [{
                    'streams': {
                        '$elemMatch': {
                            'format': {
                                '$in': formats
                            }
                        }
                    }
                }]

            
            
        # END: Build match

        # START: Find matching runIds
            
        orlist=[]
        if mode == 'OR':
            for x in aggregate_match:
                orlist.append({x:aggregate_match[x]})
            aggregate_pipeline =[
                {
                    '$match':  aggregate_match
                },
                {
                   '$group': {
                        '_id':'$runId'
                    }
                }
                

            ]

            
            print('--- aggregate_pipeline  OR --->', aggregate_pipeline)
            aggregateResults = self.lineage.aggregate(pipeline = aggregate_pipeline)

        elif mode == 'AND':

            and_query = helper.getAndQueryIndexedMetaAndParameters(key_value_pairs)

            aggregate_pipeline = [
                {
                    '$match': aggregate_match,
                },
                {   
                    '$unwind': '$streams'
                },
                {   
                    '$unwind': {
                        'path': '$streams.indexedMeta',
                        'preserveNullAndEmptyArrays': True
                    }
                },
                {   
                    '$unwind': {
                        'path': '$parameters',
                        'preserveNullAndEmptyArrays': True
                    }
                },
                {
                   '$group': {
                        '_id':'$runId',
                        'indexedMeta': { 
                            '$addToSet': "$streams.indexedMeta"    
                        },
                        'parameters': {
                            '$addToSet': "$parameters" 
                        }
                    },  
                },
                {
                    '$match': {
                        '$and': and_query
                    }
                }                                
            ]

            if formats is not None:
                print aggregate_pipeline
                aggregate_pipeline[4]['$group']['formats'] = {         
                    '$addToSet': "$streams.format"    
                }
                aggregate_pipeline[5]['$match']['$and'] += [{         
                    'formats': {
                        '$in': formats
                    }    
                }]
            print('--- aggregate_pipeline  AND --->', aggregate_pipeline)
            aggregateResults = self.lineage.aggregate(pipeline = aggregate_pipeline)

        runIds = []
        
        if aggregateResults!=None:
            for runId in aggregateResults:
                runIds.append(runId['_id'])
        # END: Find matching runIds
        
        # START: Find workflows using found runIds
        
        if types==None:
            finddic={"_id":{
                             "$in":runIds
                                     },
                    }
        else:
            finddic={"_id":{
                             "$in":runIds
                                     },
                                
                            "prov:type":{
                              "$in":types
                             }}
        print(finddic) 

        workflow_cursor = self.workflow.find(
            finddic,{
                        "startTime":1,
                        "system_id":1,
                        "description":1,
                        "workflowName":1,
                        "username":1  
                     }
        ).sort("startTime",direction=-1).skip(start).limit(limit)

        workflows=[]
        for workflow in workflow_cursor:
            workflows.append(workflow)
        # END: Find workflows using found runIds
        output=self.addLDContext({
            "runIds":workflows,
            "totalCount": len(runIds)
        })
        return output

    def getWorkflowExecution(self, start, limit, usernames):
        print('getWorkflowExecuton -->', usernames)
        # workflow = self.db[ProvenanceStore.BUNDLE_COLLECTION]

        query = {
            'username': {
                '$in': usernames
            }
        }

        workflow_cursor = self.workflow.find(
            query,
            {
                "startTime":1,
                "system_id":1,
                "description":1,
                "workflowName":1,
                "username":1  
            }
        ).sort("startTime",direction=-1).skip(start).limit(limit)

        workflow_count = self.workflow.count(query)

        workflows=[]
        for workflow in workflow_cursor:
            workflows.append(workflow)
    
        return {
            "runIds": workflows,
            "totalCount": workflow_count
        }

    def getEntitiesFilter_new(self,searchDic,keylist,mxvaluelist,mnvaluelist,start,limit,mode='OR',format=None):
        elementsDict ={}
        searchContextDic={}
        totalCount=0
        print('searchDic',searchDic,'keylist',keylist,'mxvaluelist',mxvaluelist,'mnvaluelist',mnvaluelist,'start',start,'limit',limit,'format',format,'mode',mode)

        # lineage = self.db[ProvenanceStore.LINEAGE_COLLECTION]
        
        if keylist==None:
            if format is not None:
                searchDic['streams.format'] = format

            lineage_items_cursor = self.lineage.find(
                searchDic,
                {
                    "iterationId": 1,
                    "prov_cluster":1,
                    "actedOnBehalfOf":1,
                    "name":1,
                    "runId":1,
                    "streams":1,
                    "parameters":1,
                    'startTime':1,
                    'endTime':1,
                    'errors':1,
                    'derivationIds':1,
                    'iterationId':1
                }).sort("endTime",direction=-1).skip(start).limit(limit)
            # TODO sort on endTime or startTime

            #count = self.lineage.count(searchDic) * 2 

            stream_items = []
            for lineage_item in lineage_items_cursor:
                if 'streams' in lineage_item:
                    for stream in lineage_item['streams']:
                        if 'iterationId' in lineage_item: 
                            stream['wasGeneratedBy'] = lineage_item['iterationId']
                        if 'parameters' in lineage_item: 
                            stream['parameters'] = lineage_item['parameters']
                        if 'startTime' in lineage_item: 
                            stream['startTime'] = lineage_item['startTime']
                        if 'endTime' in lineage_item: 
                            stream['endTime'] = lineage_item['endTime']
                        if 'runId' in lineage_item: 
                            stream['runId'] = lineage_item['runId']
                        if 'errors' in lineage_item: 
                            stream['errors'] = lineage_item['errors']
                        if 'derivationIds' in lineage_item: 
                            stream['derivationIds'] = lineage_item['derivationIds']
                        if 'prov_cluster' in lineage_item: 
                            stream['cluster'] = lineage_item['prov_cluster']
                        if 'actedOnBehalfOf' in lineage_item: 
                            stream['component'] = lineage_item['actedOnBehalfOf']
                        if 'name' in lineage_item: 
                            stream['functionName'] = lineage_item['name']
                        
                        if format is not None: 
                            if stream['format'] == format:
                                stream_items.append(stream)
                        else: 
                            stream_items.append(stream)

            total = self.lineage.find(searchDic,{"streams":1})
            
            for x in total:
                totalCount+=len(x["streams"])

            return(stream_items, totalCount)

        else:
            
            key_value_pairs = helper.getKeyValuePairs(keylist, mxvaluelist, mnvaluelist)
            indexed_meta_query = helper.getIndexedMetaQueryList(key_value_pairs, getSumm)

            if mode == 'OR': 
                searchDic['$or'] = indexed_meta_query
            elif mode == 'AND':
                searchDic['$and'] = searchDic['$and'] + indexed_meta_query

            aggregate_pipeline = [
                {
                    '$match':searchDic
                },
                {
                    '$sort': {
                        'endTime': 1
                    }
                },
                {
                    '$skip': start
                },
                {
                    '$limit': limit
                },
                {
                    "$unwind": "$streams" 
                },
                {
                    '$match': {
                        '$or': helper.getUnwindedStreamIndexedMetaQuery(key_value_pairs, format)
                    }
                },
                {
                    '$project': {
                        'format': '$streams.format',
                        'cluster':'$prov_cluster',
                        'component':'$actedOnBehalfOf',
                        'functionName':'$name',
                        'annotations': '$streams.annotations',
                        'content': '$streams.content',
                        'location': '$streams.location',
                        'id': '$streams.id',
                        'port': '$streams.port',
                        'wasGeneratedBy': '$iterationId',
                        'parameters': 1,
                        'startTime': 1,
                        'endTime': 1,
                        'runId': 1,
                        'errors': 1,
                        '_id':0,
                        'derivationIds': 1,
                        'size':'$streams.size',
                        'indexedMeta':'$streams.indexedMeta'
                    }
                }
            ]
            print('aggregate_pipeline:  ', aggregate_pipeline)
            try: 
                print('---- try ----')
                stream_items_cursor = self.lineage.aggregate(pipeline=aggregate_pipeline) 
            except:
                # If sorting fails remove the sort from the query
                print('---- except ----')

                aggregate_pipeline.pop(1)
                stream_items_cursor = self.lineage.aggregate(pipeline=aggregate_pipeline)        


            stream_items = []
            for stream_item in stream_items_cursor: 
                stream_items.append(stream_item)
            print('-----stream_items count : ', len(stream_items))
            # TODO check if we can get precise count
            total = self.lineage.find(searchDic,{"streams":1})
            
            for x in total:
                totalCount+=len(x["streams"])

            return(stream_items, totalCount)

    def getDataGranuleTerms(self, aggregationLevel = 'all', runIdList = [], usernameList = []):
        term_summaries = self.db[ProvenanceStore.TERM_SUMMARIES_COLLECTION]

        term_summaries_query = {}
        return_key = {}

        if aggregationLevel ==  'all':
            term_summaries_query['_id.type'] = 'all'

            return_key = {
                'type': 'all'
            }

        elif aggregationLevel ==  'runId':
            term_summaries_query['_id.type'] = 'runId_username'
            term_summaries_query['_id.runId'] = {
                '$in': runIdList
            }

            return_key = {
                'type': 'runId',
                'runIds': runIdList
            }

        elif aggregationLevel ==  'username':
            term_summaries_query['_id.type'] = 'username'
            term_summaries_query['_id.username'] = {
                '$in': usernameList
            }

            return_key = {
                'type': 'username',
                'usernames': usernameList
            }

        term_summaries_cursor = term_summaries.find(term_summaries_query)

        term_summaries_items = []

        for term_summaries_item in term_summaries_cursor:
            term_summaries_items.append(term_summaries_item)

        # If there is only one result return it. Else merge the results.
        if len(term_summaries_items) == 0:
            return {
                '_id': return_key,
                'value': {
                    'parameterMap': {},
                    'contentMap': {}
                }
            }

        elif len(term_summaries_items) == 1:
            item = term_summaries_items[0]
            item['_id'] = return_key 
            return item

        else: 
            merged_value = {
                'parameterMap': {},
                'contentMap': {}
            }
            value_maps = [ 
                'contentMap',
                'parameterMap'
            ]

            for term_summaries_item in term_summaries_items:

                for value_map in value_maps:
                    if value_map in term_summaries_item['value']:
                        for key in term_summaries_item['value'][value_map]:
                            if key not in merged_value[value_map]:
                                merged_value[value_map][key] = term_summaries_item['value'][value_map][key]
                            else:
                                merged_value[value_map][key]['count'] += term_summaries_item['value'][value_map][key]['count']
                                if 'valuesByType' in term_summaries_item['value'][value_map][key]:
                                    for value_type_key in term_summaries_item['value'][value_map][key]['valuesByType']:
                                    
                                        if value_type_key not in merged_value[value_map][key]['valuesByType']:
                                            merged_value[value_map][key]['valuesByType'][value_type_key] = term_summaries_item['value'][value_map][key]['valuesByType'][value_type_key]
                                        else:
                                            merged_value[value_map][key]['valuesByType'][value_type_key]['count'] += term_summaries_item['value'][value_map][key]['valuesByType'][value_type_key]['count']
                                            if value_type_key == 'number':
                                                if merged_value[value_map][key]['valuesByType'][value_type_key]['min'] > term_summaries_item['value'][value_map][key]['valuesByType'][value_type_key]['min']:
                                                    merged_value[value_map][key]['valuesByType'][value_type_key]['min'] = term_summaries_item['value'][value_map][key]['valuesByType'][value_type_key]['min']
                                                elif merged_value[value_map][key]['valuesByType'][value_type_key]['max'] < term_summaries_item['value'][value_map][key]['valuesByType'][value_type_key]['max']:
                                                    merged_value[value_map][key]['valuesByType'][value_type_key]['max'] = term_summaries_item['value'][value_map][key]['valuesByType'][value_type_key]['max']  
            return {
                '_id': return_key,
                'value': merged_value
            }

    def hasAncestorWith_new(self, streamId, maxDepth, keylist, minvalues, maxvalues, setContained = False,mode="OR"):
         

        start_node = self.lineage.find_one({
                'streams.id': streamId
            },
            {
                'derivationIds': 1,
                'startTime': 1,
                'runId': 1
            })

        key_value_pairs = helper.getKeyValuePairs(keylist, maxvalues, minvalues) 
        indexed_meta_query = helper.getAndQueryList(key_value_pairs)
        #print(indexed_meta_query)
        #print('--start-node->', start_node)

        # TODO use endTime or startTime

        min_date = None
        if setContained == True:
            max_startTime = start_node['startTime']
            min_possible_match_query = {
                'startTime': {
                    '$lte': start_node['startTime']
                },
                '$or': helper.getIndexedMetaQueryList(key_value_pairs),
                'runId': start_node['runId']
            }
            print('--- min_possible_match_query----->', min_possible_match_query)
            min_possible_match_cursor = self.lineage.find(min_possible_match_query).sort("startTime",direction=1).limit(1)

            min_possible_match = None
            for i in min_possible_match_cursor:
                min_possible_match = i
            print('---min_possible_match -->', min_possible_match)
            if min_possible_match == None:
                print('---return false -->', )
                return False
            else: 
                min_date = min_possible_match['startTime']

        derivationIds = []
        if 'derivationIds' in start_node:
            for derivationId in start_node['derivationIds']:
                if 'DerivedFromDatasetID' in derivationId:
                    derivationIds.append(derivationId['DerivedFromDatasetID'])

        depth = 1;
        #print('depth : ', depth, derivationIds, maxDepth,mode)
        if mode=="OR":
            mode="$or"
        else:
            mode="$and"
        while len(derivationIds) > 0 and maxDepth > 0:

            
            depth += 1 
            ancestor_match_query = {
                'streams': {
                    '$elemMatch': {
                        'id': {
                            '$in': derivationIds
                        },
                        mode: indexed_meta_query
                    }
                }
            }
            #print('depth : ', depth, derivationIds, maxDepth,ancestor_match_query)
            ancestor_match = self.lineage.find_one(ancestor_match_query, { '_id': 1 })
            #print('result : ', ancestor_match)

            if ancestor_match is not None: 
                return True

            next_level_query = {
                'streams': {
                    '$elemMatch': {
                        'id': {
                            '$in': derivationIds
                        }
                    }
                }
            }

            if setContained == True:
                next_level_query['startTime'] = {
                    '$gte': min_date
                }

            lineage_cursor = self.lineage.find(next_level_query, { 'derivationIds': 1 })

            derivationIds = []
            for lineage_item in lineage_cursor:
                if 'derivationIds' in lineage_item:
                    for derivationId in lineage_item['derivationIds']:
                        if 'DerivedFromDatasetID' in derivationId and derivationId['DerivedFromDatasetID']!=None:
                            derivationIds.append(derivationId['DerivedFromDatasetID'])
            
            maxDepth -= 1

        return False


