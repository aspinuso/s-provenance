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


import time
import helper as helper

class ProvenanceStore(object):

    def __init__(self, url):
 
        self.conection = MongoClient(url, 27017)


    # TODO Move maxDepth to kwarggs. Return ordered by levels?
    def getDerivedFrom(self, streamIdList, maxDepth, resultSet, idMap):
        db = self.conection["verce-prov"]
        lineage = db['lineage']
        
        if maxDepth < 0: 
            print('max depth reached')
            return resultSet

        find_query = {
            'streams': {
                '$elemMatch': {
                    'id': {
                        '$in': streamIdList
                    }
                }
            }
        }  
        lineage_cursor = lineage.find(find_query);

        streamIdList = []
        for lineage in lineage_cursor:
            if lineage['_id'] not in idMap:
                idMap[lineage['_id']] = 1
                resultSet.append(lineage)
                if lineage['derivationIds']:
                    for derivationId in lineage['derivationIds']:
                        if derivationId['DerivedFromDatasetID']:        
                            streamIdList.append(derivationId['DerivedFromDatasetID'])
        
        # print('maxDepth : ', 1000 - maxDepth,  ' streamIdList: ', len(streamIdList), len(list(set(streamIdList))),  )               

        if len(streamIdList) > 0:  
            streamIdList = list(set(streamIdList))
            return self.getAncestorsLevel(streamIdList, maxDepth-1, resultSet, idMap) 
        else:
            return   
