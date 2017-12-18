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

import helper as helper

import time

class ProvenanceStore(object):

    def __init__(self, url):
 
        self.connection = MongoClient(url, 27017)

    # TODO Move maxDepth to kwarggs.
    def getTraceList(self, idList, maxDepth, resultSet, idMap):
        db = self.connection["verce-prov"]
        lineage = db['lineage']
        
        if maxDepth < 0: 
            # print('max depth reached')
            return

        find_query = {
            'streams': {
                '$elemMatch': {
                    'id': {
                        '$in': idList
                    }
                }
            }
        }  
        lineage_cursor = lineage.find(find_query);

        idList = []
        for lineage in lineage_cursor:
            if lineage['_id'] not in idMap:
                idMap[lineage['_id']] = 1
                resultSet.append(lineage)
                if 'derivationIds' in lineage:
                    for derivationId in lineage['derivationIds']:
                        if 'DerivedFromDatasetID' in derivationId:        
                            idList.append(derivationId['DerivedFromDatasetID'])
        
        # print('maxDepth : ', 1000 - maxDepth,  ' idList: ', len(idList), len(list(set(idList))),  )               

        if len(idList) > 0:  
            idList = list(set(idList))
            return self.getTraceList(idList, maxDepth-1, resultSet, idMap) 
        else:
            return   


    def getTrace(self):
        # TODO implement
        return {}

    def getDerivedDataTrace(self): 
        # TODO implement
        return {}

    # TODO make kwargs explicit
    def getDataGranuleTerms(self, **kwargs):
        # TODO dataguide?
        db = self.connection["verce-prov"]
        content_summaries = db['content_summaries']

        query = {
            '_id': {

            }
        }
        _id = {}

        if 'users' in kwargs:
            if len(kwargs['users']) == 1:
                query['_id']['username'] = kwargs['users']
            else: 
                query['_id']['username'] =  {
                    '$in': kwargs['users']
                }
            _id['username'] = kwargs['users']

        elif 'runId' in kwargs:
            if len(kwargs['runId']) == 1:
                query['_id']['runId'] = kwargs['runId']
            else: 
                query['_id']['runId'] =  {
                    '$in': kwargs['runId']
                }
            _id['runId'] = kwargs['runId']

        else : 
            query = {
                'type': 'all'
            }

        content_summaries_cursors = content_summaries.find(query)
        # TODO check if you can check the length of a cursor this way
        if len(content_summaries_cursors) == 1:
            return {
                '_id': _id,
                'value': content_summaries_cursors['value']
            }
        
        summary = {}
        for content_summary in content_summaries_cursors:
            for content_key in content_summary['value']:
                if content_key not in summary:
                    summary[content_key] = content_summary['value'][content_key]
                else:
                    summary[content_key]['count'] += content_summary['value'][content_key]['count']
                    for valueType in content_summary['value'][content_key]['valuesByType']:
                        if valueType == 'number':
                            summary[content_key]['valuesByType'][valueType]['count'] += content_summary['value'][content_key]['valuesByType'][valueType]['count']
                            if summary[content_key]['valuesByType'][valueType]['min'] > content_summary['value'][content_key]['valuesByType'][valueType]['min']:
                                summary[content_key]['valuesByType'][valueType]['min'] = content_summary['value'][content_key]['valuesByType'][valueType]['min'] 
                            elif summary[content_key]['valuesByType'][valueType]['max'] < content_summary['value'][content_key]['valuesByType'][valueType]['max']:
                                summary[content_key]['valuesByType'][valueType]['max'] = content_summary['value'][content_key]['valuesByType'][valueType]['max']
                        # else:
        return summary


    def insert(self):
        from pymongo import InsertOne
        db = self.connection["verce-prov"]
        lineage = db['lineage']
        items = lineage.find({}).sort("_id",direction=1)
        lineage_new = db['lineage_new']

        # .limit(limit)
        transformedItems = []
        count = 1
        iteration = 1
        for item in items:
            print count
            count +=1
            print('---before--->', item['_id'])
                
            transformedItems.append(InsertOne(helper.addIndexedContentToLineage(item)))

            if len(transformedItems) == 100000:
                start = time.time()
                print('---before-bulk-->', start, 'iteration: ', iteration)
                iteration +=1
                lineage_new.bulk_write(transformedItems)
                end = time.time()
                print('---after-bulk-->', end-start)
                transformedItems = []


        start = time.time()
        print('---before-bulk-->', start, 'iteration: ', iteration)
        iteration +=1
        lineage_new.bulk_write(transformedItems)
        end = time.time()
        print('---after-bulk-->', end-start)

                

    def getWorkflowExecuton(self, start, limit, usernames, functionNames, keylist, maxvalues, minvalues):
        db = self.connection["verce-prov"]
        lineage = db['lineage']
        workflow = db['workflow']

        # BUILD MATCH
        aggregate_match = {}
        if usernames is not None and len(usernames) > 0: 
            aggregate_match['username'] = {
                '$in': usernames
            }

        if functionNames is not None and len(functionNames) > 0: 
            aggregate_match['name'] = {
                '$in': functionNames
            }

        key_value_pairs = helper.getKeyValuePairs(keylist, maxvalues, minvalues);

        if len(key_value_pairs) > 0:
            aggregate_match['$or'] = []
            for key_value_pair in key_value_pairs: 
                aggregate_match['$or'].append({
                    'streams': {
                        '$elemMatch': {
                            'indexedMeta': {
                                '$elemMatch': key_value_pair
                            }
                        }  
                    }  
                })
                aggregate_match['$or'].append({
                    'parameters': {
                        '$elemMatch': key_value_pair
                    }
                })
        # TODO see if sort on runId or index that end on runId have influence on the group stage.

        # GET WORKFLOW IDS
        aggregateResults = lineage.aggregate(pipeline= [
            {
                '$match': aggregate_match,
            },
            {
               '$group':{
                    '_id':'$runId'
                }
            }                                
        ])

        runIds = []
        for runId in aggregateResults:
            runIds.append(runId['_id'])

        workflowQueryResults = workflow.find(
            {
                "_id":{
                    "$in":runIds
                }
            },
            {
                "startTime":1,
                "system_id":1,
                "description":1,
                "workflowName":1 
            }
        ).sort("startTime",direction=-1).skip(start).limit(limit)

        workflows=[]
        for workflow in workflowQueryResults:
            workflows.append(workflow)
    
        return {
            "runIds":workflows,
            "totalCount": len(runIds)
        } 
               

 