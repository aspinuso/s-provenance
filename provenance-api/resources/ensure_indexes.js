// select right db

//db = db.getSiblingDB(dbName)

var indexes = [ 
    { 
        'index': {
            'streams.indexedMeta.key': 1,
            'streams.indexedMeta.val': 1
        },
        'collection': 'lineage',
        'name': 'lineage indexedMeta'
    },
    { 
        'index': {
            'parameters.key': 1,
            'parameters.val': 1
        },
        'collection': 'lineage',
        'name': 'lineage parameters'
    },    
    { 
        'index': {
            'streams.id': 1
        },
        'collection': 'lineage',
        'name': 'lineage streamsId'
    },
    { 
        'index': {
            'derivationId.DerivedFromDatasetID': 1
        },
        'collection': 'lineage',
        'name': 'lineage DerivedFromDatasetID'
    },
    { 
        'index': {
            'runId': 1
        },
        'collection': 'lineage',
        'name': 'lineage runId'
    },
    {
        'index': {
            'streams.format': 1
        },
        'collection': 'lineage',
        'name': 'lineage streams format'
    },
    {
        'index': {
            'insertedAt': 1
        },
        'collection': 'lineage',
        'name': 'lineage insertedAt'
    },
    {
        'index': {
            'interationId': 1
        },
        'collection': 'lineage',
        'name': 'lineage interationId'
    },
    {
        'index': {
            'instanceId': 1
        },
        'collection': 'lineage',
        'name': 'lineage instanceId'
    },
    {
        'index': {
            'name': 1
        },
        'collection': 'lineage',
        'name': 'lineage name'
    },
    {
        'index': {
            'username': 1
        },
        'collection': 'lineage',
        'name': 'lineage username'
    },
    {
        'index': {
            'actedOnBehalfOf': 1
        },
        'collection': 'lineage',
        'name': 'lineage actedOnBehalfOf'
    },
    {
        'index': {
            'streams.port': 1
        },
        'collection': 'lineage',
        'name': 'lineage streams port'
    },
    {
        'index': {
            'prov_cluster' : 1
        },
        'collection': 'lineage',
        'name': 'provenance clusters'
    }
]
print('start indexing')
for (let index of indexes) {
    print('creating index: ', index.name)
    db[index.collection].createIndex(index.index)
}
print('end indexing')

    