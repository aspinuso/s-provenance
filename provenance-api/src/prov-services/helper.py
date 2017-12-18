import numbers
import copy
import exceptions
import datetime

def addIndexedContentToLineage(lineage):
    MAXIMUM_STRING_SIZE_FOR_INDEXING = 50
    lineage_updated = copy.deepcopy(lineage)

    if 'streams' in lineage_updated and type(lineage_updated['streams']) == list:
        for stream in lineage_updated['streams']:
            if 'content' in stream and type(stream['content']) == list:
                all_content_map = {}
                for content in stream['content']:
                    if type(content) == dict:
                        for key in content:
                            if isinstance(content[key], numbers.Number) or ( type(content[key]) is unicode and len(content[key]) < MAXIMUM_STRING_SIZE_FOR_INDEXING):

                                if key not in all_content_map:
                                    all_content_map[key] = {}
                                    all_content_map[key][content[key]] = 1
                                else: 
                                    all_content_map[key][content[key]] = 1
          
                indexedMeta = []
                for map_key in all_content_map:
                    for map_value in all_content_map[map_key]:
                        indexedMeta.append({
                            'key': map_key,
                            'val': map_value
                        })
                stream['indexedMeta'] = indexedMeta

    if 'parameters' in lineage_updated and type(lineage_updated['parameters']) == dict:
        parametersKeyVal = []
        for key in lineage_updated['parameters']:
            parametersKeyVal.append({
                'key': key,
                'val': lineage_updated['parameters'][key]
                })
        lineage_updated['parameters'] = parametersKeyVal

    lineage_updated['insertedAt'] = datetime.datetime.now()

    return lineage_updated

def lineageToJsonLd(lineage):
    jsonLd = {}
    return jsonLd

def jsonLdToLineage():
    lineage = {}
    # TODO implement transformation of JSON-LD to lineage
    return lineage

def workflowToJsonLd(lineage):
    jsonLd = {}
    # TODO implement transformation of workflow to JSON-LD
    return jsonLd

def jsonLdToWorkflow():
    workflow = {}
    # TODO implement transformation of JSON-LD to workflow
    return workflow
    
def getIndexedMetaQueryList(KeyValuePairs, optionalFormat=None):
    indexedMetaQueryList = []
    for key_value_pair in KeyValuePairs:
        item = {
            'streams': {
                '$elemMatch': {
                    'indexedMeta': {
                        '$elemMatch': key_value_pair 
                    }
                }
            }
        }
        if optionalFormat is not None: 
            item['streams']['$elemMatch']['format'] = optionalFormat

        indexedMetaQueryList.append(item)
    return indexedMetaQueryList

def getParametersQueryList(KeyValuePairs):
    parametersQueryList = []
    for key_value_pair in KeyValuePairs:
        parametersQueryList.append({
            'parameters': {
                '$elemMatch': key_value_pair
            }
        })
    return parametersQueryList

def getAndQueryList(KeyValuePairs):
    parametersQueryList = []
    for key_value_pair in KeyValuePairs:
        parametersQueryList.append({
            'indexedMeta': {
                '$elemMatch': key_value_pair
            }
        })
    return parametersQueryList


def getUnwindedStreamIndexedMetaQuery(KeyValuePairs, optionalFormat=None):
    parametersQueryList = []
    for key_value_pair in KeyValuePairs:
        item = {
            'streams.indexedMeta': {
                '$elemMatch': key_value_pair
            }
        }
        if optionalFormat != None:
            item['streams.format'] = optionalFormat
        parametersQueryList.append(item)
    return parametersQueryList

def getKeyValuePairs(keylist, maxvalues, minvalues):
    keys = copy.deepcopy(keylist)
    maxValList = copy.deepcopy(maxvalues)
    minValList = copy.deepcopy(minvalues)

    try:
        key_val_match_list = []

        for key in keys:

            maxval=num(maxValList.pop(0))
            minval=num(minValList.pop(0))

            value = {
                '$gte': minval,
                '$lte': maxval
            }

            if maxval == minval:
                value = maxval 

            key_val_match_list.append({
                'key': key,
                'val': value
            })

        return key_val_match_list
    except exceptions.ValueError:
        # TODO how to handle error?
        return []

def num(s):
    val=None
    try:
        val= float(s)
    except exceptions.ValueError:
        try:
            val= int(s)
        except exceptions.ValueError:
            val= str(s)
    finally:
        return val

