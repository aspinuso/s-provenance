import numbers
def addIndexedContentToLineage(lineage):
  # TODO first deep-copy lineage to get rid of state
    if 'streams' in lineage and type(lineage['streams']) == list:
        for stream in lineage['streams']:
            if 'content' in stream and type(stream['content']) == list:
                all_content_map = {}
                for content in stream['content']:
                    if type(content) == dict:
                        for key in content:
                            if isinstance(content[key], numbers.Number) or ( type(content[key]) is unicode and len(content[key]) < 20):

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
                            'value': map_value
                        })
                stream['indexedMeta'] = indexedMeta
    return lineage


def lineageToJsonLd(lineage):
  jsonLd = {}
  # TODO implement transformation of lineage to JSON-LD
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


def getIndices():  
    return [ 
        { 
            'index': [
                ('streams.indexedMeta.key', ASCENDING),
                ('streams.indexedMeta.value', ASCENDING)
            ],
            'name': 'key_value'
        } 
    ]


def getKeyValuePairs(keylist, maxvalues, minvalues):
    # TODO check lengths
    items= []

    for key in keylist:

        maxval=maxvalues.pop(0)
        minval=minvalues.pop(0)

        value = {
            '$gte': minval,
            '$lte': maxval
        }

        if maxval == minval:
            value = maxval 

        items.append({
            'key': key,
            'value': value
        })

    return items


